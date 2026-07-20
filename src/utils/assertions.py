from http import HTTPStatus

from httpx import Response

NOT_FOUND_ERROR = "EntityNotFoundError"
SQLITE_CONSTRAINT_NOTNULL_ERROR_NAME = "QueryFailedError"
SQLITE_CONSTRAINT_NOTNULL_ERROR_CODE = "SQLITE_CONSTRAINT_NOTNULL"


def assert_entity_not_found(response: Response) -> None:
    assert response.status_code == HTTPStatus.BAD_REQUEST

    body = response.json()

    assert body["name"] == NOT_FOUND_ERROR, (
        f"Error name is not as expected! "
        f"Expected: {NOT_FOUND_ERROR}, "
        f"actual: {body['name']}"
    )


def assert_not_null_constraint(response: Response) -> None:
    assert response.status_code == HTTPStatus.BAD_REQUEST

    body = response.json()

    assert body["name"] == SQLITE_CONSTRAINT_NOTNULL_ERROR_NAME, (
        f"Error name is not as expected! "
        f"Expected: {SQLITE_CONSTRAINT_NOTNULL_ERROR_NAME}, "
        f"actual: {body['name']}"
    )
    assert body["code"] == SQLITE_CONSTRAINT_NOTNULL_ERROR_CODE, (
        f"Error code is not as expected! "
        f"Expected: {SQLITE_CONSTRAINT_NOTNULL_ERROR_CODE}, "
        f"actual: {body['code']}"
    )
