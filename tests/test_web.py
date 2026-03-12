from io import BytesIO
from itertools import count

from task_management.web import app, manager


def reset_manager() -> None:
    manager._tasks.clear()
    manager._ids = count(1)


def request(method: str, path: str, data: str = ""):
    body = data.encode("utf-8")
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": BytesIO(body),
    }

    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    chunks = app(environ, start_response)
    captured["body"] = b"".join(chunks)
    return captured


def test_homepage_renders_successfully():
    reset_manager()

    response = request("GET", "/")

    assert response["status"].startswith("200")
    assert b"Task Manager" in response["body"]
    assert b"/static/logo.svg" in response["body"]

    logo_response = request("GET", "/static/logo.svg")
    assert logo_response["status"].startswith("200")


def test_create_update_delete_task_via_http_endpoints():
    reset_manager()

    create_response = request("POST", "/tasks", "title=Buy+milk")
    assert create_response["status"].startswith("303")

    page = request("GET", "/")
    assert b"Buy milk" in page["body"]
    assert b"todo" in page["body"]

    update_response = request("POST", "/tasks/1/status", "status=done")
    assert update_response["status"].startswith("303")

    page_after_update = request("GET", "/")
    assert b"done" in page_after_update["body"]

    delete_response = request("POST", "/tasks/1/delete")
    assert delete_response["status"].startswith("303")

    page_after_delete = request("GET", "/")
    assert b"Buy milk" not in page_after_delete["body"]
