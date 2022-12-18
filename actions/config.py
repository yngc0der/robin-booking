class Config:
    def __init__(self,
                 selenium_webdriver_url: str,
                 robin_credentials: str,
                 robin_seats_priority: list[str],
                 robin_organization: str,
                 robin_location: str,
                 robin_level: str,
                 timezone: str
                ) -> None:
        self.__selenium_webdriver_url = selenium_webdriver_url
        self.__robin_credentials = robin_credentials
        self.__robin_seats_priority = robin_seats_priority
        self.__robin_organization = robin_organization
        self.__robin_location = robin_location
        self.__robin_level = robin_level
        self.__timezone = timezone
    
    @property
    def selenium_webdriver_url(self) -> str:
        return self.__selenium_webdriver_url

    @property
    def robin_credentials(self) -> str:
        return self.__robin_credentials

    @property
    def robin_seats_priority(self) -> str:
        return self.__robin_seats_priority

    @property
    def robin_organization(self) -> str:
        return self.__robin_organization

    @property
    def robin_location(self) -> str:
        return self.__robin_location

    @property
    def robin_level(self) -> str:
        return self.__robin_level
    
    @property
    def timezone(self) -> str:
        return self.__timezone
