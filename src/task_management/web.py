from __future__ import annotations

from pathlib import Path
from urllib.parse import parse_qs

from task_management.service import TaskManager, VALID_STATUSES

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

manager = TaskManager()


def _read_template(name: str) -> str:
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8")


def _render_index() -> bytes:
    rows = []
    statuses = sorted(VALID_STATUSES)
    for task in manager.list_tasks():
        options = "".join(
            f"<option value=\"{status}\" {'selected' if status == task.status else ''}>{status}</option>"
            for status in statuses
        )
        rows.append(
            "<tr>"
            f"<td>{task.id}</td>"
            f"<td>{task.title}</td>"
            f"<td><span class=\"status {task.status}\">{task.status}</span></td>"
            "<td>"
            f"<form action=\"/tasks/{task.id}/status\" method=\"post\" class=\"inline-form\">"
            f"<select name=\"status\">{options}</select>"
            "<button type=\"submit\">Update</button>"
            "</form>"
            "</td>"
            "<td>"
            f"<form action=\"/tasks/{task.id}/delete\" method=\"post\">"
            "<button type=\"submit\" class=\"danger\">Delete</button>"
            "</form>"
            "</td>"
            "</tr>"
        )

    html = _read_template("index.html")
    html = html.replace("{{TASK_ROWS}}", "\n".join(rows) or '<tr><td colspan="5">No tasks yet.</td></tr>')
    return html.encode("utf-8")


def _redirect(start_response):
    start_response("303 See Other", [("Location", "/")])
    return [b""]


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")

    if method == "GET" and path == "/":
        content = _render_index()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [content]

    if method == "GET" and path == "/static/styles.css":
        css = (STATIC_DIR / "styles.css").read_bytes()
        start_response("200 OK", [("Content-Type", "text/css; charset=utf-8")])
        return [css]

    if method == "POST" and path == "/tasks":
        length = int(environ.get("CONTENT_LENGTH") or 0)
        body = environ["wsgi.input"].read(length).decode("utf-8")
        title = parse_qs(body).get("title", [""])[0]
        if title.strip():
            manager.create_task(title)
        return _redirect(start_response)

    if method == "POST" and path.startswith("/tasks/") and path.endswith("/status"):
        task_id = int(path.split("/")[2])
        length = int(environ.get("CONTENT_LENGTH") or 0)
        body = environ["wsgi.input"].read(length).decode("utf-8")
        status = parse_qs(body).get("status", [""])[0]
        if status in VALID_STATUSES:
            try:
                manager.update_status(task_id, status)
            except KeyError:
                pass
        return _redirect(start_response)

    if method == "POST" and path.startswith("/tasks/") and path.endswith("/delete"):
        task_id = int(path.split("/")[2])
        try:
            manager.delete_task(task_id)
        except KeyError:
            pass
        return _redirect(start_response)

    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Not Found"]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    with make_server("0.0.0.0", 5000, app) as server:
        print("Serving on http://localhost:5000")
        server.serve_forever()
