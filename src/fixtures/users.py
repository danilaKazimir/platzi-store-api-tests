from collections.abc import AsyncIterator
from http import HTTPStatus

import pytest

from src.clients.users_client import UsersClient
from src.models.users import CreateUserRequestDto, UserResponseDto


@pytest.fixture
async def user(
    users_client: UsersClient,
) -> AsyncIterator[UserResponseDto]:
    request = CreateUserRequestDto()
    response = await users_client.create_user(request)

    assert response.status_code == HTTPStatus.CREATED

    user = UserResponseDto.model_validate_json(response.content)

    yield user

    check_user = await users_client.get_single_user(user.id)
    if check_user.status_code == HTTPStatus.OK:
        await users_client.delete_user(user.id)
