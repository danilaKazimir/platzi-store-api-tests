from http import HTTPStatus

from httpx import Response

NOT_FOUND_ERROR = "EntityNotFoundError"


def assert_user_not_found(response: Response) -> None:
    assert response.status_code == HTTPStatus.BAD_REQUEST

    body = response.json()

    assert body["name"] == NOT_FOUND_ERROR, (
        f"Error name is not as expected! "
        f"Expected: {NOT_FOUND_ERROR}, "
        f"actual: {body['name']}"
    )
