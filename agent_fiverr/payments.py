"""Escrow and payment provider runtime for marketplace checkout."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal


EscrowProvider = Literal["mock", "stripe_connect"]
EscrowStatus = Literal["held", "planned"]


@dataclass(frozen=True)
class PaymentProviderSpec:
    provider_id: EscrowProvider
    name: str
    credential_env: str | None
    capabilities: tuple[str, ...]
    live_enabled: bool = False


@dataclass(frozen=True)
class EscrowHold:
    hold_id: str
    provider_id: EscrowProvider
    status: EscrowStatus
    mode: str
    order_id: str
    quote_id: str
    buyer_id: str
    amount_usd: int
    currency: str
    created_at: str
    credential_env: str | None
    credential_configured: bool
    call_plan: dict[str, Any] = field(default_factory=dict)


class EscrowRuntime:
    def __init__(self, default_provider: EscrowProvider = "mock"):
        self.default_provider = default_provider

    def provider_report(self) -> list[dict[str, Any]]:
        return [
            {
                "provider_id": spec.provider_id,
                "name": spec.name,
                "credential_env": spec.credential_env,
                "credential_configured": _credential_configured(spec),
                "capabilities": list(spec.capabilities),
                "live_enabled": spec.live_enabled,
            }
            for spec in _PAYMENT_PROVIDERS.values()
        ]

    def hold_funds(
        self,
        *,
        order_id: str,
        quote_id: str,
        buyer_id: str,
        amount_usd: int,
        provider_id: EscrowProvider | None = None,
        currency: str = "usd",
        dry_run: bool = True,
    ) -> EscrowHold:
        provider = provider_id or self.default_provider
        spec = payment_provider_for(provider)
        if amount_usd <= 0:
            raise ValueError("Escrow amount must be positive.")
        if currency.lower() != "usd":
            raise ValueError("Only USD escrow is supported in the alpha runtime.")
        credential_configured = _credential_configured(spec)
        if provider != "mock" and not dry_run and spec.credential_env and not credential_configured:
            raise PermissionError(f"Payment provider {provider} requires {spec.credential_env}.")

        status: EscrowStatus = "held" if provider == "mock" else "planned"
        mode = "mock" if provider == "mock" else ("dry_run" if dry_run else "planned")
        return EscrowHold(
            hold_id=str(uuid.uuid4()),
            provider_id=provider,
            status=status,
            mode=mode,
            order_id=order_id,
            quote_id=quote_id,
            buyer_id=buyer_id,
            amount_usd=amount_usd,
            currency=currency.lower(),
            created_at=_now(),
            credential_env=spec.credential_env,
            credential_configured=credential_configured,
            call_plan=_call_plan(spec, dry_run=dry_run),
        )


def payment_provider_for(provider_id: EscrowProvider) -> PaymentProviderSpec:
    try:
        return _PAYMENT_PROVIDERS[provider_id]
    except KeyError as exc:
        raise KeyError(f"No payment provider scaffold registered for {provider_id}.") from exc


def _credential_configured(spec: PaymentProviderSpec) -> bool:
    return bool(spec.credential_env and os.environ.get(spec.credential_env))


def _call_plan(spec: PaymentProviderSpec, *, dry_run: bool) -> dict[str, Any]:
    return {
        "provider": spec.provider_id,
        "provider_name": spec.name,
        "credential_env": spec.credential_env,
        "required_capabilities": list(spec.capabilities),
        "live_call_allowed": bool(not dry_run and spec.live_enabled),
        "live_call_status": "dry_run" if dry_run else ("ready" if spec.live_enabled else "not_implemented"),
        "operator_note": (
            "Payment provider scaffold records escrow intent and credential "
            "requirements, but does not create external payment objects until "
            "the provider is explicitly enabled."
        ),
    }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


_PAYMENT_PROVIDERS: dict[EscrowProvider, PaymentProviderSpec] = {
    "mock": PaymentProviderSpec(
        provider_id="mock",
        name="Local Mock Escrow",
        credential_env=None,
        capabilities=("hold", "release", "refund", "dispute_marker"),
        live_enabled=True,
    ),
    "stripe_connect": PaymentProviderSpec(
        provider_id="stripe_connect",
        name="Stripe Connect Escrow Scaffold",
        credential_env="STRIPE_SECRET_KEY",
        capabilities=("payment_intent", "manual_capture", "transfer", "refund", "dispute_evidence"),
    ),
}
