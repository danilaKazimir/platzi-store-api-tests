from httpx import Response

from src.clients.http_client import HttpClient
from src.models.users import CreateUser


class UsersClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._client = http_client
        self._path = "users/"

    async def get_all_users(self) -> Response:
        return await self._client.get(self._path)

    async def get_single_user(self, user_id: int) -> Response:
        return await self._client.get(f"{self._path}{user_id}")

    async def create_user(self, request: CreateUser) -> Response:
        return await self._client.post(self._path, json=request.model_dump(mode="json"))
