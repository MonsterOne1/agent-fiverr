"""Trust ledger export for replaying order fulfillment evidence."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from .order import Order


@dataclass(frozen=True)
class TrustLedger:
    order_id: str
    service_slug: str
    current_state: str
    audit_events: list[dict[str, Any]]
    deliverable_versions: list[dict[str, Any]]
    revision_requests: list[dict[str, Any]]
    provider_traces: list[dict[str, Any]]
    escrow_events: list[dict[str, Any]]
    qa_results: list[dict[str, Any]]
    replay_counts: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_trust_ledger(
    order: Order,
    *,
    provider_traces: Iterable[Any] = (),
    escrow_events: Iterable[Any] = (),
    qa_results: Iterable[Any] = (),
) -> TrustLedger:
    provider_records = [_record(item) for item in provider_traces]
    escrow_records = [_record(item) for item in escrow_events]
    qa_records = [_record(item) for item in qa_results]
    audit_events = [asdict(item) for item in order.audit]
    deliverables = [asdict(item) for item in order.deliverables]
    revisions = [asdict(item) for item in order.revisions]
    return TrustLedger(
        order_id=order.order_id,
        service_slug=order.service_slug,
        current_state=order.state,
        audit_events=audit_events,
        deliverable_versions=deliverables,
        revision_requests=revisions,
        provider_traces=provider_records,
        escrow_events=escrow_records,
        qa_results=qa_records,
        replay_counts={
            "audit_events": len(audit_events),
            "deliverable_versions": len(deliverables),
            "revision_requests": len(revisions),
            "provider_traces": len(provider_records),
            "escrow_events": len(escrow_records),
            "qa_results": len(qa_records),
        },
    )


def _record(item: Any) -> dict[str, Any]:
    if hasattr(item, "__dataclass_fields__"):
        return asdict(item)
    if isinstance(item, dict):
        return dict(item)
    raise TypeError(f"Unsupported trust ledger item: {type(item)!r}")
