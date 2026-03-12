# Task Management System (Starter)

This repository now contains a starter task management system implemented in Python.

## Features

- Create tasks with title and optional description
- List all tasks or filter by status
- Update task status (`todo`, `in_progress`, `done`)
- Delete tasks

## Project structure

- `src/task_management/models.py` — task data model and statuses
- `src/task_management/service.py` — in-memory task manager service
- `tests/test_task_manager.py` — initial unit tests

## Run tests

```bash
PYTHONPATH=src pytest -q
```
