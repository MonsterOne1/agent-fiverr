"""Provider adapter registry with dry-run, credential gates, and call plans."""

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
    adapter: dict[str, Any] = field(default_factory=dict)
    call_plan: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderAdapterSpec:
    provider_id: str
    actions: dict[str, tuple[str, ...]]
    scopes: tuple[str, ...]
    artifact_types: tuple[str, ...]
    live_enabled: bool = False

    def required_fields(self, action: str) -> tuple[str, ...]:
        if action == "simulate_provider_output":
            return ("sample_id",)
        try:
            return self.actions[action]
        except KeyError as exc:
            allowed = ", ".join(sorted([*self.actions, "simulate_provider_output"]))
            raise ValueError(f"Action {action} is not supported by {self.provider_id}. Allowed: {allowed}.") from exc

    def validate_request(self, action: str, request: dict[str, Any]) -> list[str]:
        return [field for field in self.required_fields(action) if not request.get(field)]


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
        adapter = adapter_for(provider_id)
        missing_request_fields = adapter.validate_request(action, request)
        if missing_request_fields:
            raise ValueError(
                f"Provider {provider_id} action {action} missing request fields: "
                f"{', '.join(missing_request_fields)}."
            )
        if not dry_run and credential.required and not credential.configured:
            raise PermissionError(f"Provider {provider_id} requires {credential.credential_env}.")

        status = "dry_run" if dry_run else "planned"
        return ProviderTrace(
            provider_id=provider_id,
            action=action,
            status=status,
            side_effect_level=provider["side_effect_level"],
            timestamp=datetime.now(timezone.utc).isoformat(),
            request=request,
            asset_manifest=_asset_manifest(provider_id, action, request, adapter, dry_run=dry_run),
            adapter=_adapter_manifest(adapter),
            call_plan=_call_plan(provider, credential, adapter, action, dry_run=dry_run),
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


def adapter_for(provider_id: str) -> ProviderAdapterSpec:
    try:
        return _ADAPTERS[provider_id]
    except KeyError as exc:
        raise KeyError(f"No provider adapter scaffold registered for {provider_id}.") from exc


def _asset_manifest(
    provider_id: str,
    action: str,
    request: dict[str, Any],
    adapter: ProviderAdapterSpec,
    *,
    dry_run: bool,
) -> dict[str, Any]:
    return {
        "provider": provider_id,
        "action": action,
        "mode": "dry_run" if dry_run else "planned",
        "artifact_types": list(adapter.artifact_types),
        "request_keys": sorted(request.keys()),
        "rights_notes": "Provider/source notes must be retained for generated assets.",
    }


def _adapter_manifest(adapter: ProviderAdapterSpec) -> dict[str, Any]:
    return {
        "provider": adapter.provider_id,
        "actions": sorted([*adapter.actions, "simulate_provider_output"]),
        "scopes": list(adapter.scopes),
        "artifact_types": list(adapter.artifact_types),
        "live_enabled": adapter.live_enabled,
    }


def _call_plan(
    provider: dict[str, Any],
    credential: CredentialStatus,
    adapter: ProviderAdapterSpec,
    action: str,
    *,
    dry_run: bool,
) -> dict[str, Any]:
    return {
        "provider": provider["id"],
        "provider_name": provider["name"],
        "action": action,
        "credential_env": credential.credential_env,
        "credential_configured": credential.configured,
        "side_effect_level": provider["side_effect_level"],
        "required_scopes": list(adapter.scopes),
        "live_call_allowed": bool(not dry_run and adapter.live_enabled),
        "live_call_status": "dry_run" if dry_run else ("ready" if adapter.live_enabled else "not_implemented"),
        "operator_note": (
            "This scaffold validates inputs and credentials, but does not send "
            "network calls until the provider adapter is explicitly enabled."
        ),
    }


_ADAPTERS: dict[str, ProviderAdapterSpec] = {
    "openai_responses": ProviderAdapterSpec(
        provider_id="openai_responses",
        actions={
            "draft_text": ("prompt", "service_slug"),
            "analyze": ("prompt", "source_material"),
            "qa_review": ("deliverable", "rubric"),
        },
        scopes=("model.responses",),
        artifact_types=("markdown", "json", "document"),
    ),
    "gpt_image_2": ProviderAdapterSpec(
        provider_id="gpt_image_2",
        actions={
            "generate_image": ("prompt", "size", "usage_rights"),
            "edit_image": ("prompt", "source_asset", "usage_rights"),
        },
        scopes=("model.images",),
        artifact_types=("png", "asset_manifest"),
    ),
    "banana": ProviderAdapterSpec(
        provider_id="banana",
        actions={
            "generate_image": ("prompt", "aspect_ratio", "usage_rights"),
            "edit_image": ("prompt", "source_asset", "usage_rights"),
        },
        scopes=("image.generate", "image.edit"),
        artifact_types=("png", "asset_manifest"),
    ),
    "seedance": ProviderAdapterSpec(
        provider_id="seedance",
        actions={
            "generate_video": ("prompt", "duration_seconds", "aspect_ratio", "usage_rights"),
            "image_to_video": ("prompt", "source_asset", "duration_seconds", "usage_rights"),
        },
        scopes=("video.generate",),
        artifact_types=("mp4", "storyboard", "asset_manifest"),
    ),
    "kling": ProviderAdapterSpec(
        provider_id="kling",
        actions={
            "generate_video": ("prompt", "duration_seconds", "aspect_ratio", "usage_rights"),
            "image_to_video": ("prompt", "source_asset", "duration_seconds", "usage_rights"),
        },
        scopes=("video.generate",),
        artifact_types=("mp4", "asset_manifest"),
    ),
    "renoise": ProviderAdapterSpec(
        provider_id="renoise",
        actions={
            "direct_video": ("brief", "shot_list", "usage_rights"),
            "download_reference": ("source_url", "usage_rights"),
        },
        scopes=("video.direct", "asset.download"),
        artifact_types=("mp4", "shot_list", "asset_manifest"),
    ),
    "suno": ProviderAdapterSpec(
        provider_id="suno",
        actions={
            "generate_music": ("prompt", "duration_seconds", "usage_rights"),
            "generate_jingle": ("prompt", "brand_notes", "duration_seconds", "usage_rights"),
        },
        scopes=("music.generate",),
        artifact_types=("wav", "mp3", "license_notes"),
    ),
    "elevenlabs": ProviderAdapterSpec(
        provider_id="elevenlabs",
        actions={
            "generate_voiceover": ("script", "voice_id", "usage_rights"),
            "dub_audio": ("source_asset", "target_language", "usage_rights"),
        },
        scopes=("voice.generate", "voice.dub"),
        artifact_types=("wav", "mp3", "transcript", "license_notes"),
    ),
    "browser_search": ProviderAdapterSpec(
        provider_id="browser_search",
        actions={
            "research": ("query", "source_policy"),
            "seo_scan": ("url", "source_policy"),
        },
        scopes=("network.read",),
        artifact_types=("markdown", "csv", "source_log"),
    ),
    "github": ProviderAdapterSpec(
        provider_id="github",
        actions={
            "inspect_repo": ("repo", "task"),
            "open_pull_request": ("repo", "branch", "summary", "authorization_id"),
        },
        scopes=("repo.read", "repo.write"),
        artifact_types=("patch", "pull_request", "audit_log"),
    ),
    "vercel": ProviderAdapterSpec(
        provider_id="vercel",
        actions={
            "create_preview": ("project", "branch", "authorization_id"),
            "inspect_deployment": ("deployment_url", "authorization_id"),
        },
        scopes=("deployment.read", "deployment.write"),
        artifact_types=("preview_url", "deployment_log"),
    ),
    "wordpress": ProviderAdapterSpec(
        provider_id="wordpress",
        actions={
            "draft_post": ("site_url", "title", "content", "authorization_id"),
            "edit_page": ("site_url", "page_id", "changes", "authorization_id"),
        },
        scopes=("cms.read", "cms.write"),
        artifact_types=("cms_draft", "audit_log"),
    ),
    "shopify": ProviderAdapterSpec(
        provider_id="shopify",
        actions={
            "draft_product": ("store_url", "product_payload", "authorization_id"),
            "edit_theme": ("store_url", "theme_id", "changes", "authorization_id"),
        },
        scopes=("store.read", "store.write"),
        artifact_types=("store_draft", "theme_patch", "audit_log"),
    ),
    "google_ads": ProviderAdapterSpec(
        provider_id="google_ads",
        actions={
            "keyword_plan": ("customer_id", "seed_keywords", "authorization_id"),
            "draft_campaign": ("customer_id", "campaign_brief", "authorization_id"),
        },
        scopes=("ads.read", "ads.write"),
        artifact_types=("csv", "campaign_draft", "audit_log"),
    ),
}
