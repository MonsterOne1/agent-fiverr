"""Minimal order/workroom runtime for service-agent fulfillment."""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .catalog import Catalog


LifecycleState = Literal[
    "intake",
    "scope_check",
    "quote",
    "plan",
    "work",
    "qa",
    "delivery",
    "revision",
    "close",
    "memory",
]

LIFECYCLE: tuple[LifecycleState, ...] = (
    "intake",
    "scope_check",
    "quote",
    "plan",
    "work",
    "qa",
    "delivery",
    "revision",
    "close",
    "memory",
)

AUTHORIZATION_REQUIRED_LEVELS = {"requires_explicit_authorization"}


@dataclass
class AuditEvent:
    timestamp: str
    kind: str
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DeliverableVersion:
    version: int
    created_at: str
    payload: dict[str, Any]
    qa_score: int
    qa_notes: list[str]


@dataclass
class RevisionRequest:
    request_id: str
    created_at: str
    description: str
    in_scope: bool
    reason: str


@dataclass
class Order:
    order_id: str
    service_slug: str
    brief: dict[str, Any]
    state: LifecycleState
    missing_brief_fields: list[str] = field(default_factory=list)
    authorizations: dict[str, bool] = field(default_factory=dict)
    audit: list[AuditEvent] = field(default_factory=list)
    deliverables: list[DeliverableVersion] = field(default_factory=list)
    revisions: list[RevisionRequest] = field(default_factory=list)


class OrderRuntime:
    def __init__(self, root: Path, catalog: Catalog | None = None):
        self.root = root
        self.catalog = catalog or Catalog(root)
        self.orders_dir = root / "workrooms"
        self.orders_dir.mkdir(parents=True, exist_ok=True)

    def create_order(self, service_slug: str, brief: dict[str, Any]) -> Order:
        self.catalog.get_service(service_slug)
        missing = self.catalog.validate_brief(service_slug, brief)
        order = Order(
            order_id=str(uuid.uuid4()),
            service_slug=service_slug,
            brief=brief,
            state="intake",
            missing_brief_fields=missing,
        )
        self._audit(order, "order_created", "Order created from buyer brief.")
        if missing:
            self._audit(
                order,
                "brief_incomplete",
                "Brief is missing required fields.",
                {"missing_fields": missing},
            )
        self.save(order)
        return order

    def load(self, order_id: str) -> Order:
        path = self._order_path(order_id)
        if not path.exists():
            raise FileNotFoundError(f"Unknown order: {order_id}")
        data = json.loads(path.read_text(encoding="utf-8"))
        return Order(
            order_id=data["order_id"],
            service_slug=data["service_slug"],
            brief=data["brief"],
            state=data["state"],
            missing_brief_fields=data.get("missing_brief_fields", []),
            authorizations=data.get("authorizations", {}),
            audit=[AuditEvent(**event) for event in data.get("audit", [])],
            deliverables=[DeliverableVersion(**item) for item in data.get("deliverables", [])],
            revisions=[RevisionRequest(**item) for item in data.get("revisions", [])],
        )

    def save(self, order: Order) -> None:
        self._order_path(order.order_id).write_text(
            json.dumps(asdict(order), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def transition(self, order: Order, target: LifecycleState) -> Order:
        current_index = LIFECYCLE.index(order.state)
        target_index = LIFECYCLE.index(target)
        if target_index != current_index + 1:
            raise ValueError(f"Invalid transition: {order.state} -> {target}")
        if order.missing_brief_fields and target not in {"scope_check"}:
            raise ValueError("Cannot advance beyond scope_check with missing brief fields.")
        order.state = target
        self._audit(order, "state_transition", f"Order moved to {target}.")
        self.save(order)
        return order

    def authorize(self, order: Order, gate: str) -> Order:
        order.authorizations[gate] = True
        self._audit(order, "authorization_granted", f"Authorization granted for {gate}.")
        self.save(order)
        return order

    def require_provider_action(self, order: Order, provider: str, action: str) -> None:
        side_effects = self.catalog.provider_side_effect_levels(order.service_slug)
        if provider not in side_effects:
            raise ValueError(f"Provider {provider} is not configured for {order.service_slug}.")
        level = side_effects[provider]
        gate = f"{provider}:{action}"
        if level in AUTHORIZATION_REQUIRED_LEVELS and not order.authorizations.get(gate):
            self._audit(
                order,
                "authorization_blocked",
                f"Blocked {provider} action without explicit authorization.",
                {"provider": provider, "action": action, "gate": gate},
            )
            self.save(order)
            raise PermissionError(f"Explicit authorization required for {gate}.")
        self._audit(order, "provider_action_allowed", f"Allowed {provider} action {action}.")
        self.save(order)

    def add_deliverable(
        self,
        order: Order,
        payload: dict[str, Any],
        qa_score: int,
        qa_notes: list[str],
    ) -> Order:
        if qa_score < 4:
            self._audit(order, "delivery_blocked", "Deliverable blocked by QA threshold.", {"qa_score": qa_score})
            self.save(order)
            raise ValueError("Deliverable QA score must be 4 or higher.")
        version = len(order.deliverables) + 1
        order.deliverables.append(
            DeliverableVersion(
                version=version,
                created_at=_now(),
                payload=payload,
                qa_score=qa_score,
                qa_notes=qa_notes,
            )
        )
        self._audit(order, "deliverable_added", f"Deliverable version {version} added.", {"qa_score": qa_score})
        self.save(order)
        return order

    def request_revision(self, order: Order, description: str, changed_fields: list[str]) -> RevisionRequest:
        service = self.catalog.get_service(order.service_slug)
        in_scope = not any(field not in service.brief_fields for field in changed_fields)
        reason = "within original brief" if in_scope else "changes fields outside original brief"
        revision = RevisionRequest(
            request_id=str(uuid.uuid4()),
            created_at=_now(),
            description=description,
            in_scope=in_scope,
            reason=reason,
        )
        order.revisions.append(revision)
        self._audit(
            order,
            "revision_requested",
            "Revision request recorded.",
            {"in_scope": in_scope, "changed_fields": changed_fields},
        )
        self.save(order)
        return revision

    def _audit(self, order: Order, kind: str, message: str, metadata: dict[str, Any] | None = None) -> None:
        order.audit.append(AuditEvent(timestamp=_now(), kind=kind, message=message, metadata=metadata or {}))

    def _order_path(self, order_id: str) -> Path:
        return self.orders_dir / f"{order_id}.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

