from typing import Any

from httpx import AsyncClient, Response

from settings import settings
from src.utils.http_hooks import log_request, log_response


class HttpClient:
    def __init__(self) -> None:
        super().__init__()
        self._client = AsyncClient(
            base_url=settings.BASE_URL,
            timeout=settings.TIMEOUT,
            event_hooks={
                "request": [log_request],
                "response": [log_response],
            },
        )

    async def __aenter__(self) -> "HttpClient":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Response:
        return await self._client.request(
            method, path, json=json, headers=headers, **kwargs
        )

    async def get(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Response:
        return await self._request("GET", path, headers=headers, **kwargs)

    async def post(
        self,
        path: str,
        *,
        json: dict[str, Any],
        **kwargs: Any,
    ) -> Response:
        return await self._request("POST", path, json=json, **kwargs)

    async def put(self, path: str, *, json: dict[str, Any], **kwargs: Any) -> Response:
        return await self._request("PUT", path, json=json, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Response:
        return await self._request("DELETE", path, **kwargs)
