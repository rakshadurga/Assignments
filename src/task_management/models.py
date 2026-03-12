from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass(slots=True)
class Task:
    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = field(default_factory=datetime.utcnow)

    def mark_in_progress(self) -> None:
        self.status = TaskStatus.IN_PROGRESS

    def mark_done(self) -> None:
        self.status = TaskStatus.DONE
