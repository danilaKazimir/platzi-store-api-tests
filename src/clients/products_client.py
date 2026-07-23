from httpx import Response

from src.clients.http_client import HttpClient
from src.models.products import CreateProductRequestDto


class ProductsClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._client = http_client
        self._path = "products/"

    async def get_single_product(self, product_id: int) -> Response:
        return await self._client.get(f"{self._path}{product_id}")

    async def create_product(self, request: CreateProductRequestDto) -> Response:
        return await self._client.post(
            f"{self._path}", json=request.model_dump(mode="json")
        )
