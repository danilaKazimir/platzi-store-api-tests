import pytest

pytest_plugins = ["src.fixtures.clients", "src.fixtures.users"]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
