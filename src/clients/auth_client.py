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
