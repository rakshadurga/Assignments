from task_management import TaskManager, TaskStatus


def test_create_and_list_tasks_sorted() -> None:
    manager = TaskManager()
    manager.create_task("Write specs")
    manager.create_task("Implement service")

    tasks = list(manager.list_tasks())

    assert [task.id for task in tasks] == [1, 2]
    assert [task.title for task in tasks] == ["Write specs", "Implement service"]


def test_update_and_filter_by_status() -> None:
    manager = TaskManager()
    todo = manager.create_task("Backlog")
    in_progress = manager.create_task("Current")

    manager.update_status(in_progress.id, TaskStatus.IN_PROGRESS)

    filtered = list(manager.list_tasks(status=TaskStatus.IN_PROGRESS))

    assert len(filtered) == 1
    assert filtered[0].id == in_progress.id
    assert filtered[0].status == TaskStatus.IN_PROGRESS
    assert todo.status == TaskStatus.TODO


def test_delete_task() -> None:
    manager = TaskManager()
    task = manager.create_task("Temporary")

    manager.delete_task(task.id)

    assert list(manager.list_tasks()) == []
