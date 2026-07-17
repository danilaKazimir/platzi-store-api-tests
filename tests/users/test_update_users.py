from http import HTTPStatus

import pytest

from src.clients.users_client import UsersClient
from src.models.users import UpdateUserRequestDto, UserResponseDto
from src.utils.assertions.users_assertions import assert_user_not_found


@pytest.mark.anyio
class TestUpdateUsers:
    NOT_FOUND_USER_ID = 0

    @pytest.mark.parametrize(
        "request_dto",
        [
            UpdateUserRequestDto(),
            UpdateUserRequestDto(email=None),
            UpdateUserRequestDto(name=None),
        ],
    )
    async def test_update_user(
        self,
        user: UserResponseDto,
        users_client: UsersClient,
        request_dto: UpdateUserRequestDto,
    ) -> None:
        response = await users_client.update_user(user.id, request_dto)
        assert response.status_code == HTTPStatus.OK

        response_model = UserResponseDto.model_validate_json(response.content)
        if request_dto.name:
            assert response_model.name == request_dto.name
        else:
            assert response_model.name == user.name
        if request_dto.email:
            assert response_model.email == request_dto.email
        else:
            assert response_model.email == user.email
        assert response_model.model_dump(
            exclude={"name", "email", "updated_at"}
        ) == user.model_dump(exclude={"name", "email", "updated_at"})

    async def test_update_non_existent_user(self, users_client: UsersClient) -> None:
        response = await users_client.update_user(
            self.NOT_FOUND_USER_ID, UpdateUserRequestDto()
        )
        assert_user_not_found(response)
