from typing import Optional

class Response:
    def __init__(
        self,
        body: Optional[str],
        headers: dict[str, str],
        ok: bool,
        redirected: bool,
        status: int,
        status_text: str,
        type: str,
        url: str
    ) -> None:
        self.__headers = headers
        self.__body = body
        self.__ok = ok
        self.__redirected = redirected
        self.__status = status
        self.__status_text = status_text
        self.__type = type
        self.__url = url
    
    @property
    def headers(self) -> str:
        return self.__headers
    
    @property
    def body(self) -> str:
        return self.__body
    
    @property
    def ok(self) -> str:
        return self.__ok
    
    @property
    def redirected(self) -> str:
        return self.__redirected
    
    @property
    def status(self) -> str:
        return self.__status
    
    @property
    def status_text(self) -> str:
        return self.__status_text
    
    @property
    def type(self) -> str:
        return self.__type

    @property
    def url(self) -> str:
        return self.__url
