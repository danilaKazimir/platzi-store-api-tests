from httpx import Response

from src.clients.http_client import HttpClient
from src.models.auth import LoginRequestDto


class AuthClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._client = http_client
        self._path = "auth/"

    async def login(self, request: LoginRequestDto) -> Response:
        return await self._client.post(
            f"{self._path}login", json=request.model_dump(mode="json")
        )

    async def retrieving_user_profile(self, access_token: str) -> Response:
        headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
        return await self._client.get(f"{self._path}profile", headers=headers)

    async def refresh_token(self, refresh_token: str) -> Response:
        return await self._client.post(
            f"{self._path}refresh-token", json={"refreshToken": refresh_token}
        )
