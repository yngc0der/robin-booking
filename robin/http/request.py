from typing import Optional
from robin import JsonDict

class Request:
    def __init__(
        self,
        method: str,
        url: str,
        mode: Optional[str]=None,
        cache: Optional[str]=None,
        credentials: Optional[str]=None,
        headers: Optional[dict[str, str]]=None,
        redirect: Optional[str]=None,
        referrer_policy: Optional[str]=None,
        body: Optional[str]=None
    ) -> None:
        self.__method = method
        self.__url = url
        self.__mode = mode
        self.__cache = cache
        self.__credentials = credentials
        self.__headers = headers
        self.__redirect = redirect
        self.__referrer_policy = referrer_policy
        self.__body = body
    
    @property
    def method(self) -> str:
        return self.__method

    @property
    def url(self) -> str:
        return self.__url

    @property
    def mode(self) -> Optional[str]:
        return self.__mode
    
    @property
    def cache(self) -> Optional[str]:
        return self.__cache

    @property
    def credentials(self) -> Optional[str]:
        return self.__credentials

    @property
    def headers(self) -> Optional[dict[str, str]]:
        return self.__headers

    @property
    def redirect(self) -> Optional[str]:
        return self.__redirect

    @property
    def referrer_policy(self) -> Optional[str]:
        return self.__referrer_policy

    @property
    def body(self) -> Optional[str]:
        return self.__body
