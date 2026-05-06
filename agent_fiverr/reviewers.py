"""Reviewer pool and assignment policy for human QA escalation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .catalog import Catalog
from .qa import HumanReviewItem, HumanReviewQueue


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Reviewer:
    reviewer_id: str
    name: str
    specialties: tuple[str, ...]
    max_open_reviews: int
    active: bool = True


@dataclass(frozen=True)
class AssignmentDecision:
    review_id: str
    reviewer_id: str
    reason: str
    open_review_count: int


class ReviewerPool:
    def __init__(self, reviewers: list[Reviewer], catalog: Catalog):
        self.reviewers = reviewers
        self.catalog = catalog

    @classmethod
    def load(cls, root: Path = ROOT, path: Path | None = None) -> "ReviewerPool":
        source = path or (root / "data" / "reviewer-pool.example.json")
        records = json.loads(source.read_text(encoding="utf-8"))
        reviewers = [
            Reviewer(
                reviewer_id=record["reviewer_id"],
                name=record["name"],
                specialties=tuple(record["specialties"]),
                max_open_reviews=record["max_open_reviews"],
                active=record.get("active", True),
            )
            for record in records
        ]
        return cls(reviewers, Catalog(root))

    def assign(self, queue: HumanReviewQueue, review_id: str) -> AssignmentDecision:
        item = _find_review(queue, review_id)
        open_counts = _open_counts(queue)
        reviewer, reason = self._select_reviewer(item, open_counts)
        queue.assign(review_id, reviewer.reviewer_id)
        return AssignmentDecision(
            review_id=review_id,
            reviewer_id=reviewer.reviewer_id,
            reason=reason,
            open_review_count=open_counts.get(reviewer.reviewer_id, 0),
        )

    def _select_reviewer(self, item: HumanReviewItem, open_counts: dict[str, int]) -> tuple[Reviewer, str]:
        service = self.catalog.get_service(item.service_slug)
        active = [reviewer for reviewer in self.reviewers if reviewer.active]
        eligible = [
            reviewer
            for reviewer in active
            if open_counts.get(reviewer.reviewer_id, 0) < reviewer.max_open_reviews
        ]
        if not eligible:
            raise RuntimeError("No reviewer capacity available.")

        direct = [
            reviewer
            for reviewer in eligible
            if service.slug in reviewer.specialties or service.category in reviewer.specialties
        ]
        candidates = direct or eligible
        selected = sorted(candidates, key=lambda reviewer: (open_counts.get(reviewer.reviewer_id, 0), reviewer.reviewer_id))[0]
        reason = "specialty_match" if selected in direct else "general_capacity"
        return selected, reason


def _find_review(queue: HumanReviewQueue, review_id: str) -> HumanReviewItem:
    for item in queue.items:
        if item.review_id == review_id:
            return item
    raise KeyError(f"Unknown review: {review_id}")


def _open_counts(queue: HumanReviewQueue) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in queue.pending():
        if item.reviewer_id:
            counts[item.reviewer_id] = counts.get(item.reviewer_id, 0) + 1
    return counts
