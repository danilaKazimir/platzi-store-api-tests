import logging
import os
from datetime import datetime
from pathlib import Path

import allure
import pytest
from xdist import is_xdist_controller  # type: ignore[import-untyped]

pytest_plugins = [
    "src.fixtures.clients",
    "src.fixtures.users",
    "src.fixtures.categories",
    "src.fixtures.products",
]


def pytest_configure() -> None:
    logging.getLogger("http_client").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


@pytest.fixture
@allure.title("Set asyncio tests run mode")
def anyio_backend() -> str:
    return "asyncio"


def pytest_sessionstart(session: pytest.Session) -> None:
    if is_xdist_controller(session):
        return

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")

    worker_id = os.getenv("PYTEST_XDIST_WORKER")
    worker_suffix = f"_{worker_id}" if worker_id else ""

    log_path = Path(f"logs/pytest_{timestamp}{worker_suffix}.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    plugin = session.config.pluginmanager.get_plugin("logging-plugin")

    if plugin is not None:
        logging_plugin = plugin
        logging_plugin.set_log_path(str(log_path))
