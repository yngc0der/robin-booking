from typing import Optional
from actions import AbstractAction, ActionError
from robin import ApiClient, JsonDict
from robin.http import HttpClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class CheckinAction(AbstractAction):
    def exec(self) -> None:
        with HttpClient.create_webdriver(self._config.selenium_webdriver_url) as driver:
            api_client = ApiClient(HttpClient(driver))

            organization = api_client.organization(self._config.robin_organization).data
            
            api_client.authenticate(self._config.robin_credentials, organization["id"])

            user = api_client.me().data

            location = self.__find_location(
                api_client.locations(organization["id"], {
                    "query": self._config.robin_location,
                    "page": 1,
                    "per_page": 150
                }).data,
                self._config.robin_location
            )

            if location is None:
                raise ActionError("Location is not found")

            level = self.__find_level(
                api_client.location_levels(location["id"], {
                    "page": 1,
                    "per_page": 150
                }).data,
                self._config.robin_level
            )

            if level is None:
                raise ActionError("Location level is not found")

            checkin_from, checkin_to = self.__get_checkin_dates(ZoneInfo(self._config.timezone))

            reservations = api_client.reservations_seats({
                "level_ids": level["id"],
                "user_ids": user["id"],
                "after": checkin_from.isoformat(),
                "before": checkin_to.isoformat(),
                "page": 1,
                "per_page": 2000
            }).data

            for reservation in reservations:
                if reservation["confirmation"] is not None:
                    continue

                api_client.confirm_reservation(reservation["id"], {
                    "user_id": user["id"],
                })

    def __get_checkin_dates(self, tz: ZoneInfo) -> tuple[datetime, datetime]:
        checkin_date = datetime.now(tz).replace(microsecond=0) - timedelta(minutes=30)
        return (checkin_date.astimezone(ZoneInfo("UTC")), (checkin_date + timedelta(hours=1)).astimezone(ZoneInfo("UTC")))

    def __find_location(self, locations: list[JsonDict], name: str) -> Optional[JsonDict]:
        for location in locations:
            if location["name"] == name:
                return location
        return None

    def __find_level(self, levels: list[JsonDict], name: str) -> Optional[JsonDict]:
        for level in levels:
            if level["name"] == name:
                return level
        return None
