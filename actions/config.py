class Config:
    def __init__(self,
                 selenium_webdriver_url: str,
                 robin_credentials: str,
                 robin_user_id: int,
                 robin_organization_id: int,
                 robin_space_id: int,
                 robin_level_id: int,
                 robin_seats_priority: list[str],
                 timezone: str
                ) -> None:
        self.__selenium_webdriver_url = selenium_webdriver_url
        self.__robin_credentials = robin_credentials
        self.__robin_user_id = robin_user_id
        self.__robin_organization_id = robin_organization_id
        self.__robin_space_id = robin_space_id
        self.__robin_level_id = robin_level_id
        self.__robin_seats_priority = robin_seats_priority
        self.__timezone = timezone
    
    @property
    def selenium_webdriver_url(self) -> str:
        return self.__selenium_webdriver_url

    @property
    def robin_credentials(self) -> str:
        return self.__robin_credentials

    @property
    def robin_user_id(self) -> str:
        return self.__robin_user_id
    
    @property
    def robin_organization_id(self) -> str:
        return self.__robin_organization_id
    
    @property
    def robin_space_id(self) -> str:
        return self.__robin_space_id
    
    @property
    def robin_level_id(self) -> str:
        return self.__robin_level_id
    
    @property
    def robin_seats_priority(self) -> str:
        return self.__robin_seats_priority
    
    @property
    def timezone(self) -> str:
        return self.__timezone
