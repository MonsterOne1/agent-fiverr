"""Automatic QA evaluation and human review queue."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

from .catalog import Catalog


QAStatus = Literal["pass", "human_review", "block"]


@dataclass(frozen=True)
class QAResult:
    service_slug: str
    status: QAStatus
    score: int
    missing_fields: tuple[str, ...]
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class HumanReviewItem:
    review_id: str
    order_id: str
    service_slug: str
    qa_result: QAResult
    status: str
    created_at: str


@dataclass
class HumanReviewQueue:
    items: list[HumanReviewItem] = field(default_factory=list)

    def enqueue(self, order_id: str, service_slug: str, qa_result: QAResult) -> HumanReviewItem:
        item = HumanReviewItem(
            review_id=str(uuid.uuid4()),
            order_id=order_id,
            service_slug=service_slug,
            qa_result=qa_result,
            status="open",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.items.append(item)
        return item


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

