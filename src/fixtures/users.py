
import pytest

from src.clients.users_client import UsersClient


@pytest.fixture
def user(
    users_client: UsersClient,
) -> None:
    pass
