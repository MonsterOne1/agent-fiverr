"""Automatic QA evaluation and human review workflow."""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

from .catalog import Catalog


QAStatus = Literal["pass", "human_review", "block"]
ReviewDecision = Literal["approved", "changes_requested", "rejected"]
ReviewStatus = Literal["open", "assigned", "approved", "changes_requested", "rejected"]


@dataclass(frozen=True)
class QAResult:
    service_slug: str
    status: QAStatus
    score: int
    missing_fields: tuple[str, ...]
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class HumanReviewDecisionRecord:
    decision: ReviewDecision
    reviewer_id: str
    notes: str
    decided_at: str


@dataclass(frozen=True)
class HumanReviewItem:
    review_id: str
    order_id: str
    service_slug: str
    qa_result: QAResult
    status: ReviewStatus
    created_at: str
    sla_due_at: str
    reviewer_id: str | None = None
    assigned_at: str | None = None
    decision: HumanReviewDecisionRecord | None = None


@dataclass
class HumanReviewQueue:
    items: list[HumanReviewItem] = field(default_factory=list)

    def enqueue(
        self,
        order_id: str,
        service_slug: str,
        qa_result: QAResult,
        *,
        sla_hours: int = 24,
    ) -> HumanReviewItem:
        created_at = _now()
        item = HumanReviewItem(
            review_id=str(uuid.uuid4()),
            order_id=order_id,
            service_slug=service_slug,
            qa_result=qa_result,
            status="open",
            created_at=created_at,
            sla_due_at=(datetime.fromisoformat(created_at) + timedelta(hours=sla_hours)).isoformat(),
        )
        self.items.append(item)
        return item

    def assign(self, review_id: str, reviewer_id: str) -> HumanReviewItem:
        item = self._get(review_id)
        if item.status not in {"open", "assigned"}:
            raise ValueError(f"Review {review_id} is already decided.")
        updated = replace(
            item,
            status="assigned",
            reviewer_id=reviewer_id,
            assigned_at=_now(),
        )
        self._replace(updated)
        return updated

    def decide(
        self,
        review_id: str,
        *,
        decision: ReviewDecision,
        reviewer_id: str,
        notes: str,
    ) -> HumanReviewItem:
        item = self._get(review_id)
        if item.status == "open":
            raise ValueError(f"Review {review_id} must be assigned before decision.")
        if item.status != "assigned":
            raise ValueError(f"Review {review_id} is already decided.")
        if item.reviewer_id != reviewer_id:
            raise PermissionError(f"Review {review_id} is assigned to {item.reviewer_id}.")
        updated = replace(
            item,
            status=decision,
            decision=HumanReviewDecisionRecord(
                decision=decision,
                reviewer_id=reviewer_id,
                notes=notes,
                decided_at=_now(),
            ),
        )
        self._replace(updated)
        return updated

    def pending(self) -> list[HumanReviewItem]:
        return [item for item in self.items if item.status in {"open", "assigned"}]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json_dumps([_item_to_record(item) for item in self.items]),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "HumanReviewQueue":
        if not path.exists():
            return cls()
        records = json_loads(path.read_text(encoding="utf-8"))
        return cls(items=[_item_from_record(record) for record in records])

    def _get(self, review_id: str) -> HumanReviewItem:
        for item in self.items:
            if item.review_id == review_id:
                return item
        raise KeyError(f"Unknown review: {review_id}")

    def _replace(self, updated: HumanReviewItem) -> None:
        for index, item in enumerate(self.items):
            if item.review_id == updated.review_id:
                self.items[index] = updated
                return
        raise KeyError(f"Unknown review: {updated.review_id}")


class QAEvaluator:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    def evaluate(
        self,
        service_slug: str,
        payload: dict[str, object],
        *,
        risk_override: str | None = None,
    ) -> QAResult:
        service = self.catalog.get_service(service_slug)
        missing = tuple(field for field in service.output_fields if not payload.get(field))
        reasons: list[str] = []

        if missing:
            reasons.append("deliverable schema missing required fields")
            return QAResult(
                service_slug=service_slug,
                status="block",
                score=2,
                missing_fields=missing,
                reasons=tuple(reasons),
            )

        risk = risk_override or service.risk_level
        if risk == "high":
            reasons.append("high risk service requires human review before delivery")
            return QAResult(
                service_slug=service_slug,
                status="human_review",
                score=4,
                missing_fields=(),
                reasons=tuple(reasons),
            )

        reasons.append("deliverable schema complete")
        reasons.extend(service.qa_checks)
        return QAResult(
            service_slug=service_slug,
            status="pass",
            score=4 if service.risk_level == "medium" else 5,
            missing_fields=(),
            reasons=tuple(reasons),
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _item_to_record(item: HumanReviewItem) -> dict[str, Any]:
    return asdict(item)


def _item_from_record(record: dict[str, Any]) -> HumanReviewItem:
    qa = record["qa_result"]
    decision = record.get("decision")
    return HumanReviewItem(
        review_id=record["review_id"],
        order_id=record["order_id"],
        service_slug=record["service_slug"],
        qa_result=QAResult(
            service_slug=qa["service_slug"],
            status=qa["status"],
            score=qa["score"],
            missing_fields=tuple(qa.get("missing_fields", [])),
            reasons=tuple(qa.get("reasons", [])),
        ),
        status=record["status"],
        created_at=record["created_at"],
        sla_due_at=record["sla_due_at"],
        reviewer_id=record.get("reviewer_id"),
        assigned_at=record.get("assigned_at"),
        decision=HumanReviewDecisionRecord(**decision) if decision else None,
    )


def json_dumps(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def json_loads(value: str) -> Any:
    return json.loads(value)
