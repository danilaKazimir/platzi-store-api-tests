from httpx import Response

from src.clients.http_client import HttpClient
from src.models.products import CreateProductRequestDto, UpdateProductRequestDto


class ProductsClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._client = http_client
        self._path = "products/"

    async def get_all_products(
        self, offset: int | None = None, limit: int | None = None
    ) -> Response:
        query_params = {"offset": offset, "limit": limit}
        return await self._client.get(f"{self._path}", query_params=query_params)

    async def get_single_product_by_id(self, product_id: int) -> Response:
        return await self._client.get(f"{self._path}{product_id}")

    async def get_products_related_by_id(self, product_id: int) -> Response:
        return await self._client.get(f"{self._path}{product_id}/related")

    async def get_single_product_by_slug(self, slug: str) -> Response:
        return await self._client.get(f"{self._path}slug/{slug}")

    async def get_products_related_by_slug(self, slug: str) -> Response:
        return await self._client.get(f"{self._path}slug/{slug}/related")

    async def create_product(self, request: CreateProductRequestDto) -> Response:
        return await self._client.post(
            f"{self._path}", json=request.model_dump(mode="json")
        )

    async def update_product(
        self, product_id: int, request: UpdateProductRequestDto
    ) -> Response:
        return await self._client.put(
            f"{self._path}{product_id}", json=request.model_dump(mode="json")
        )

    async def delete_product(self, product_id: int) -> Response:
        return await self._client.delete(f"{self._path}{product_id}")
