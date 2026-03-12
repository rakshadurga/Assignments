from __future__ import annotations

from collections.abc import Iterable

from .models import Task, TaskStatus


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create_task(self, title: str, description: str = "") -> Task:
        if not title.strip():
            raise ValueError("title cannot be empty")

        task = Task(id=self._next_id, title=title.strip(), description=description.strip())
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(self, *, status: TaskStatus | None = None) -> Iterable[Task]:
        tasks = self._tasks.values()
        if status is None:
            return sorted(tasks, key=lambda task: task.id)
        return [task for task in sorted(tasks, key=lambda task: task.id) if task.status == status]

    def get_task(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as error:
            raise KeyError(f"task {task_id} does not exist") from error

    def update_status(self, task_id: int, status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        task.status = status
        return task

    def delete_task(self, task_id: int) -> None:
        if task_id not in self._tasks:
            raise KeyError(f"task {task_id} does not exist")
        del self._tasks[task_id]
