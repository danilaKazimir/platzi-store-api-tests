from collections.abc import AsyncIterator

import allure
import pytest

from src.clients.auth_client import AuthClient
from src.clients.categories_client import CategoriesClient
from src.clients.http_client import HttpClient
from src.clients.users_client import UsersClient


@pytest.fixture
@allure.title("Initializing http client")
async def http_client() -> AsyncIterator[HttpClient]:
    async with HttpClient() as client:
        yield client


@pytest.fixture
@allure.title("Initializing users client")
def users_client(http_client: HttpClient) -> UsersClient:
    return UsersClient(http_client)


@pytest.fixture
@allure.title("Initializing categories client")
def categories_client(http_client: HttpClient) -> CategoriesClient:
    return CategoriesClient(http_client)


@pytest.fixture
@allure.title("Initializing auth client")
def auth_client(http_client: HttpClient) -> AuthClient:
    return AuthClient(http_client)
