from collections.abc import AsyncIterator

import pytest

from src.clients.http_client import HttpClient
from src.clients.users_client import UsersClient


@pytest.fixture
async def http_client() -> AsyncIterator[HttpClient]:
    async with HttpClient() as client:
        yield client


@pytest.fixture
def users_client(http_client: HttpClient) -> UsersClient:
    return UsersClient(http_client)
