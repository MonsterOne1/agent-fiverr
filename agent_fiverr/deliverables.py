"""Structured deliverable packaging for document, table, and widget outputs."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal


DeliverableSurface = Literal["document", "table", "widget"]


@dataclass(frozen=True)
class PackagedDeliverable:
    order_id: str
    surface: DeliverableSurface
    title: str
    path: str
    manifest_path: str
    mime_type: str
    metadata: dict[str, Any]


class DeliverablePackager:
    def __init__(self, root: Path):
        self.root = root

    def package(
        self,
        *,
        order_id: str,
        surface: DeliverableSurface,
        title: str,
        content: Any,
        metadata: dict[str, Any] | None = None,
    ) -> PackagedDeliverable:
        target_dir = self.root / "workrooms" / order_id / "deliverables"
        target_dir.mkdir(parents=True, exist_ok=True)
        if surface == "document":
            path = target_dir / "document.md"
            path.write_text(_document_markdown(title, content), encoding="utf-8")
            mime_type = "text/markdown"
        elif surface == "table":
            path = target_dir / "table.csv"
            _write_table(path, content)
            mime_type = "text/csv"
        elif surface == "widget":
            path = target_dir / "widget.html"
            path.write_text(_widget_html(title, content), encoding="utf-8")
            mime_type = "text/html"
        else:
            raise ValueError(f"Unsupported deliverable surface: {surface}")

        packaged = PackagedDeliverable(
            order_id=order_id,
            surface=surface,
            title=title,
            path=str(path.relative_to(self.root)),
            manifest_path=str((target_dir / "manifest.json").relative_to(self.root)),
            mime_type=mime_type,
            metadata=metadata or {},
        )
        (target_dir / "manifest.json").write_text(
            json.dumps(asdict(packaged), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return packaged


def _document_markdown(title: str, content: Any) -> str:
    if isinstance(content, str):
        body = content
    elif isinstance(content, dict):
        body = "\n".join(f"## {key}\n\n{value}" for key, value in content.items())
    else:
        raise TypeError("Document content must be a string or mapping.")
    return f"# {title}\n\n{body}\n"


def _write_table(path: Path, content: Any) -> None:
    if not isinstance(content, list) or not content:
        raise TypeError("Table content must be a non-empty list of row mappings.")
    if not all(isinstance(row, dict) for row in content):
        raise TypeError("Every table row must be a mapping.")
    fieldnames = list(content[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(content)


def _widget_html(title: str, content: Any) -> str:
    if not isinstance(content, dict):
        raise TypeError("Widget content must be a mapping.")
    data = json.dumps(content, indent=2, ensure_ascii=False)
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\"><title>"
        f"{_escape(title)}</title></head>\n"
        "<body>\n"
        f"<main data-agent-fiverr-widget=\"true\"><h1>{_escape(title)}</h1>"
        f"<pre>{_escape(data)}</pre></main>\n"
        "</body>\n"
        "</html>\n"
    )


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
