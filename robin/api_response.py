from __future__ import annotations
from robin.http import Response
from robin import JsonDict
from typing import Optional
import json

class ApiResponse:
    def create_from_http_response(http_response: Response) -> ApiResponse:
        data = json.loads(http_response.body)
        return ApiResponse(data["data"], data["meta"], data["paging"] if "paging" in data else None)

    def __init__(self, data: JsonDict, meta: JsonDict, paging: Optional[JsonDict]) -> None:
        self.__data = data
        self.__meta = meta
        self.__paging = paging
    
    @property
    def data(self) -> JsonDict:
        return self.__data

    @property
    def meta(self) -> JsonDict:
        return self.__meta

    @property
    def paging(self) -> Optional[JsonDict]:
        return self.__paging

    @property
    def is_success(self) -> bool:
        return self.meta["status_code"] in [200, 201]
