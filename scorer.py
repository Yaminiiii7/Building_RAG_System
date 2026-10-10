"""Simple scoring for the campus-life evaluation questions.

The evaluation harness calls `judge(question, expects, answer, results) -> bool`.
This scorer checks whether an answer contains the fact that the question was
written to expect, using a forgiving normalization so minor wording and
punctuation differences still count as correct.
"""

from __future__ import annotations

import re
from typing import Iterable


def _normalize(text: str) -> str:
    """Lowercase and squash punctuation into spaces for robust comparisons."""
    if not text:
        return ""
    text = text.lower()
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _terms(text: str) -> list[str]:
    """Return the useful content words from a phrase or answer."""
    normalized = _normalize(text)
    if not normalized:
        return []
    keep = []
    for token in normalized.split():
        if token in {"the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "with", "by", "is", "it", "at", "if", "when", "what", "how", "from", "that", "this", "be", "as", "after", "before", "than", "into", "out", "are", "was", "were", "can", "students", "student", "course", "questions"}:
            continue
        keep.append(token)
    return keep


def _contains_phrase(answer: str, phrase: str) -> bool:
    """Check for a direct normalized phrase match."""
    if not phrase:
        return True
    answer_norm = _normalize(answer)
    phrase_norm = _normalize(phrase)
    if not phrase_norm:
        return True
    if phrase_norm in answer_norm:
        return True

    # Handle common punctuation variants such as "800-character" vs "800 character"
    # and quotes around a single-letter value such as "W" on the transcript.
    if phrase_norm.replace(" ", "") in answer_norm.replace(" ", ""):
        return True

    return False


def _match_keywords(answer: str, expects: str) -> bool:
    """Use keyword coverage as a fallback when exact phrase matching fails."""
    if not expects:
        return True

    answer_terms = set(_terms(answer))
    expected_terms = _terms(expects)
    if not expected_terms:
        return True

    if not answer_terms:
        return False

    matched = sum(1 for term in expected_terms if term in answer_terms)
    required = max(1, min(len(expected_terms), 2))
    return matched >= required


def judge(question: str, expects: str, answer: str, results: Iterable[object]) -> bool:
    """Return True when an answer contains the expected fact.

    The function is intentionally tolerant:
    - it ignores punctuation/case differences,
    - it accepts the exact phrase when present,
    - and it falls back to keyword coverage for short factual phrases.

    `results` is accepted for compatibility with `run_eval.py`; it is not needed
    for the simple phrase-based scoring used here.
    """
    if answer is None:
        return False

    text = str(answer).strip()
    if not text:
        return False

    refusal_starts = (
        "i don't have enough information",
        "i don't know",
        "i can\'t answer",
        "not enough information",
        "the corpus does not cover",
        "unable to determine",
    )
    lowered = text.lower()
    if lowered.startswith(refusal_starts):
        return False

    if _contains_phrase(text, expects):
        return True

    if _match_keywords(text, expects):
        return True

    # Some answers phrase the fact in a slightly different but equivalent form,
    # such as "8th week" instead of "week eight" or "18-minute walk" instead of
    # "18 minutes". We accept a few common numeric-word equivalences here.
    answer_norm = _normalize(text)
    expects_norm = _normalize(expects)
    if expects_norm:
        for left, right in (
            ("week eight", "week 8"),
            ("week 8", "week eight"),
            ("18 minutes", "18 minute"),
            ("18 minute", "18 minutes"),
            ("800 characters", "800 character"),
            ("800 character", "800 characters"),
            ("first ten days", "first 10 days"),
            ("first 10 days", "first ten days"),
        ):
            if left in answer_norm and right in expects_norm:
                return True
            if right in answer_norm and left in expects_norm:
                return True

    return False
