"""v5 interview session state helpers.

These utilities keep the v5 platform backend-agnostic. They can be used by
static builders today and by a FastAPI service later without changing the data
contract.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any


@dataclass
class SessionTurn:
    question_id: str
    prompt: str
    candidate_answer: str = ""
    score: int | None = None
    feedback: list[str] = field(default_factory=list)
    followups: list[str] = field(default_factory=list)


@dataclass
class InterviewSession:
    session_id: str
    role: str
    domain: str
    difficulty: str
    status: str = "not_started"
    current_index: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    turns: list[SessionTurn] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def new_session(session_id: str, role: str, domain: str, difficulty: str, questions: list[dict[str, Any]]) -> InterviewSession:
    turns = []
    for q in questions:
        turns.append(
            SessionTurn(
                question_id=str(q.get("id", q.get("question_id", "unknown"))),
                prompt=str(q.get("title") or q.get("problem") or q.get("prompt") or "Practice question"),
                followups=list(q.get("followups", q.get("follow_up_questions", [])) or []),
            )
        )
    return InterviewSession(session_id=session_id, role=role, domain=domain, difficulty=difficulty, turns=turns)


def write_session(path: Path, session: InterviewSession) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(session.to_dict(), indent=2), encoding="utf-8")
