from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from typing import Iterable


VALID_STATUSES = {"todo", "in_progress", "done"}


@dataclass
class Task:
    id: int
    title: str
    status: str = "todo"


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._ids = count(1)

    def list_tasks(self) -> Iterable[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def create_task(self, title: str) -> Task:
        cleaned = title.strip()
        if not cleaned:
            raise ValueError("Task title cannot be empty")
        task = Task(id=next(self._ids), title=cleaned)
        self._tasks[task.id] = task
        return task

    def update_status(self, task_id: int, status: str) -> Task:
        if status not in VALID_STATUSES:
            raise ValueError(f"Unsupported status: {status}")
        task = self._tasks[task_id]
        task.status = status
        return task

    def delete_task(self, task_id: int) -> None:
        del self._tasks[task_id]
