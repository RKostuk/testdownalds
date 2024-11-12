from typing import Any, Optional

from rest_framework import status
from rest_framework.response import Response


def api_ok_200(obj: dict[Any, Any], headers: Optional[dict[str, str]] = None,
               content_type: str | None = None) -> Response:
    return Response(obj, status=status.HTTP_200_OK, headers=headers, content_type=content_type)


def api_created_201(obj: dict[Any, Any], headers: Optional[dict[str, str]] = None,
                    content_type: str | None = None) -> Response:
    return Response(obj, status=status.HTTP_201_CREATED, headers=headers, content_type=content_type)


def api_bad_request_400(obj: Optional[dict[Any, Any]], headers: Optional[dict[str, str]] = None,
                        content_type: str | None = None) -> Response:
    return Response(obj, status=status.HTTP_400_BAD_REQUEST, headers=headers, content_type=content_type)
