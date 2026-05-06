"""Provider adapter registry with dry-run and credential gates."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .catalog import Catalog


@dataclass(frozen=True)
class CredentialStatus:
    provider_id: str
    name: str
    credential_env: str | None
    required: bool
    configured: bool


@dataclass(frozen=True)
class ProviderTrace:
    provider_id: str
    action: str
    status: str
    side_effect_level: str
    timestamp: str
    request: dict[str, Any]
    asset_manifest: dict[str, Any] = field(default_factory=dict)


class ProviderRuntime:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    def credential_report(self, service_slug: str) -> list[CredentialStatus]:
        service = self.catalog.get_service(service_slug)
        providers = self.catalog.providers
        return [
            _credential_status(providers[provider_id])
            for provider_id in service.api_providers
        ]

    def run(
        self,
        service_slug: str,
        provider_id: str,
        action: str,
        request: dict[str, Any],
        *,
        dry_run: bool,
    ) -> ProviderTrace:
        service = self.catalog.get_service(service_slug)
        if provider_id not in service.api_providers:
            raise ValueError(f"Provider {provider_id} is not allowed for {service_slug}.")
        provider = self.catalog.providers[provider_id]
        credential = _credential_status(provider)
        if not dry_run and credential.required and not credential.configured:
            raise PermissionError(f"Provider {provider_id} requires {credential.credential_env}.")

        status = "dry_run" if dry_run else "ready"
        return ProviderTrace(
            provider_id=provider_id,
            action=action,
            status=status,
            side_effect_level=provider["side_effect_level"],
            timestamp=datetime.now(timezone.utc).isoformat(),
            request=request,
            asset_manifest=_asset_manifest(provider_id, action, request, dry_run=dry_run),
        )


def _credential_status(provider: dict[str, Any]) -> CredentialStatus:
    env_name = provider.get("credential_env")
    required = env_name is not None
    configured = bool(env_name and os.environ.get(env_name))
    return CredentialStatus(
        provider_id=provider["id"],
        name=provider["name"],
        credential_env=env_name,
        required=required,
        configured=configured,
    )


def _asset_manifest(provider_id: str, action: str, request: dict[str, Any], *, dry_run: bool) -> dict[str, Any]:
    return {
        "provider": provider_id,
        "action": action,
        "mode": "dry_run" if dry_run else "ready",
        "request_keys": sorted(request.keys()),
        "rights_notes": "Provider/source notes must be retained for generated assets.",
    }

