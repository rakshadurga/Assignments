# Task Management Web App

A lightweight web app with a WSGI entrypoint for creating and managing tasks in-memory.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest
```

## Run

```bash
PYTHONPATH=src python -m task_management.web
```

Open: <http://localhost:5000>

## Notes

- Data is stored in-memory using a shared `TaskManager` instance.
- Tasks reset whenever the app process restarts.

## Test

```bash
python -m pytest
```
