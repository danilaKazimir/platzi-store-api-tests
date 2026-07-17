import json
import logging

from httpx import Request, Response

logger = logging.getLogger("http_client")

SENSITIVE_FIELDS = {
    "password",
    "token",
    "access_token",
    "refresh_token",
}


def format_body(content: bytes) -> str:
    if not content:
        return "<empty>"

    try:
        body = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return content.decode(errors="replace")

    if isinstance(body, dict):
        for field in SENSITIVE_FIELDS:
            if field in body:
                body[field] = "***"

    return json.dumps(body, indent=2, ensure_ascii=False)


async def log_request(request: Request) -> None:
    logger.info(
        "HTTP REQUEST: %s %s\nBody:\n%s \n",
        request.method,
        request.url,
        format_body(request.content),
    )


async def log_response(response: Response) -> None:
    await response.aread()

    logger.info(
        "HTTP RESPONSE: %s %s -> %s\nBody:\n%s \n",
        response.request.method,
        response.request.url,
        response.status_code,
        format_body(response.content),
    )
