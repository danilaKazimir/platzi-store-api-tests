from httpx import Response

from src.clients.http_client import HttpClient
from src.models.categories import CreateCategoryRequestDto, UpdateCategoryRequestDto


class CategoriesClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._client = http_client
        self._path = "categories/"

    async def get_all_categories(self) -> Response:
        return await self._client.get(self._path)

    async def get_category_by_id(self, category_id: int) -> Response:
        return await self._client.get(f"{self._path}{category_id}")

    async def create_category(self, request: CreateCategoryRequestDto) -> Response:
        return await self._client.post(self._path, json=request.model_dump(mode="json"))

    async def update_category(
        self, category_id: int, request: UpdateCategoryRequestDto
    ) -> Response:
        return await self._client.put(
            f"{self._path}{category_id}", json=request.model_dump(mode="json")
        )

    async def delete_category(self, category_id: int) -> Response:
        return await self._client.delete(f"{self._path}{category_id}")
