"""Ratings, Review Metadata & Source Preservation Module

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 03 — Stage 03: Brand Taxonomy & Metadata Preservation

Maintains strict separation between expert evaluations (0-10 scale),
aggregated user feedback (0-5 score, review counts), and raw review snippets.
Preserves exact editorial review excerpts and source URLs without modification.
"""

from dataclasses import dataclass, field
import math
import re
from typing import Any, Dict, Final, List, Optional, Tuple

from .config import (
    FLAG_INVALID_EXPERT_RATING,
    FLAG_INVALID_USER_RATING,
    FLAG_MISSING_EXPERT_RATING,
    FLAG_MISSING_REVIEW_SNIPPET,
    FLAG_MISSING_REVIEW_URL,
    FLAG_MISSING_USER_RATING,
    FLAG_REVIEW_SNIPPET_WITHOUT_URL,
    FLAG_REVIEW_URL_WITHOUT_SNIPPET,
    FLAG_UNPARSEABLE_FORMAT,
    FLAG_UNPARSEABLE_USER_RATING,
)

# Deterministic User Rating Extraction Regexes
USER_SCORE_REGEX: Final[re.Pattern] = re.compile(r"(\d+(?:\.\d+)?)\s*★")
USER_COUNT_REGEX: Final[re.Pattern] = re.compile(
    r"★[\s\r\n]*([\d\.,]+[KMBL]?)\s*Ratings?", re.IGNORECASE
)


@dataclass(frozen=True)
class UserRatingResult:
    """Structured representation of parsed consumer star ratings and review volume."""

    score: Optional[float]
    count: Optional[int]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ReviewResult:
    """Exact preservation of editorial review snippet and source canonical URL."""

    snippet: Optional[str]
    url: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class RatingsMetadata:
    """Consolidated ratings, review metadata, and audit flags for a smartphone listing."""

    expert_rating: Optional[float]
    user_rating: UserRatingResult
    review: ReviewResult
    all_quality_flags: List[str] = field(default_factory=list)


def parse_expert_rating(val: Any) -> Tuple[Optional[float], List[str]]:
    """Parse technical expert rating on a 0.0 to 10.0 scale.

    Returns:
        Tuple of (expert_score, quality_flags).
        If missing or null, returns (None, [FLAG_MISSING_EXPERT_RATING]).
    """
    if val is None:
        return None, [FLAG_MISSING_EXPERT_RATING]

    if isinstance(val, float) and math.isnan(val):
        return None, [FLAG_MISSING_EXPERT_RATING]

    raw_str = str(val).strip()
    if not raw_str or raw_str.lower() in ("nan", "none", "null"):
        return None, [FLAG_MISSING_EXPERT_RATING]

    try:
        score = float(raw_str)
        if 0.0 <= score <= 10.0:
            return round(score, 2), []
        else:
            return None, [FLAG_INVALID_EXPERT_RATING]
    except (ValueError, TypeError):
        return None, [FLAG_INVALID_EXPERT_RATING]


def parse_user_rating(val: Any) -> UserRatingResult:
    """Parse composite user rating string containing star rating and review count.

    Handles formats such as:
    - '4.3 ★\r\n25.3K Ratings' -> score: 4.3, count: 25300
    - '4.2 ★\r\n1.1L Ratings'  -> score: 4.2, count: 110000 (Indian Lakh system: 1L = 100,000)
    - '4.6 ★\r\n1,921 Ratings' -> score: 4.6, count: 1921
    """
    if val is None:
        return UserRatingResult(
            score=None,
            count=None,
            raw_input=None,
            quality_flags=[FLAG_MISSING_USER_RATING],
        )

    if isinstance(val, float) and math.isnan(val):
        return UserRatingResult(
            score=None,
            count=None,
            raw_input=None,
            quality_flags=[FLAG_MISSING_USER_RATING],
        )

    raw_str = str(val).strip()
    if not raw_str or raw_str.lower() in ("nan", "none", "null"):
        return UserRatingResult(
            score=None,
            count=None,
            raw_input=raw_str if raw_str else None,
            quality_flags=[FLAG_MISSING_USER_RATING],
        )

    score_match = USER_SCORE_REGEX.search(raw_str)
    count_match = USER_COUNT_REGEX.search(raw_str)

    if not score_match or not count_match:
        return UserRatingResult(
            score=None,
            count=None,
            raw_input=raw_str,
            quality_flags=[FLAG_INVALID_USER_RATING],
        )

    try:
        score = float(score_match.group(1))
    except ValueError:
        return UserRatingResult(
            score=None,
            count=None,
            raw_input=raw_str,
            quality_flags=[FLAG_INVALID_USER_RATING],
        )

    raw_cnt = count_match.group(1).replace(",", "").strip().upper()
    try:
        if raw_cnt.endswith("K"):
            count = int(round(float(raw_cnt[:-1]) * 1000))
        elif raw_cnt.endswith("L"):
            count = int(round(float(raw_cnt[:-1]) * 100000))
        elif raw_cnt.endswith("M"):
            count = int(round(float(raw_cnt[:-1]) * 1000000))
        elif raw_cnt.endswith("B"):
            count = int(round(float(raw_cnt[:-1]) * 1000000000))
        else:
            count = int(float(raw_cnt))
    except (ValueError, TypeError):
        return UserRatingResult(
            score=score,
            count=None,
            raw_input=raw_str,
            quality_flags=[FLAG_INVALID_USER_RATING],
        )

    return UserRatingResult(
        score=score,
        count=count,
        raw_input=raw_str,
        quality_flags=[],
    )


def parse_review(snippet_val: Any, url_val: Any) -> ReviewResult:
    """Preserve verbatim editorial review snippet and source review URL.

    Guarantees:
    - Zero modification or summarization of text.
    - Exact preservation of original URL.
    - Explicit flags when review text or URL is missing, or asymmetrically unpaired.
    """
    # Process review snippet
    snippet: Optional[str] = None
    if snippet_val is not None and not (isinstance(snippet_val, float) and math.isnan(snippet_val)):
        s = str(snippet_val).strip()
        if s and s.lower() not in ("nan", "none", "null"):
            snippet = s

    # Process review URL
    url: Optional[str] = None
    if url_val is not None and not (isinstance(url_val, float) and math.isnan(url_val)):
        u = str(url_val).strip()
        if u and u.lower() not in ("nan", "none", "null"):
            url = u

    flags: List[str] = []
    has_snippet = snippet is not None
    has_url = url is not None

    if not has_snippet and not has_url:
        flags.append(FLAG_MISSING_REVIEW_SNIPPET)
        flags.append(FLAG_MISSING_REVIEW_URL)
    elif has_snippet and not has_url:
        flags.append(FLAG_MISSING_REVIEW_URL)
        flags.append(FLAG_REVIEW_SNIPPET_WITHOUT_URL)
    elif not has_snippet and has_url:
        flags.append(FLAG_MISSING_REVIEW_SNIPPET)
        flags.append(FLAG_REVIEW_URL_WITHOUT_SNIPPET)

    return ReviewResult(
        snippet=snippet,
        url=url,
        quality_flags=flags,
    )


def parse_all_ratings_and_reviews(row: Dict[str, Any]) -> RatingsMetadata:
    """Coordinate full parsing of expert ratings, user ratings, and reviews from a raw record dictionary."""
    expert_score, expert_flags = parse_expert_rating(row.get("expert_rating"))
    user_res = parse_user_rating(row.get("user_rating"))
    review_res = parse_review(row.get("review"), row.get("review_link"))

    all_flags: List[str] = []
    all_flags.extend(expert_flags)
    all_flags.extend(user_res.quality_flags)
    all_flags.extend(review_res.quality_flags)

    return RatingsMetadata(
        expert_rating=expert_score,
        user_rating=user_res,
        review=review_res,
        all_quality_flags=all_flags,
    )
