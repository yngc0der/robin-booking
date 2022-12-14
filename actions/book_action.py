from actions import AbstractAction, ActionError
from robin import ApiClient, JsonDict
from robin.http import HttpClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional

class BookAction(AbstractAction):
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

            seats = self.__get_sorted_by_priority_seats(
                api_client.seats(organization["id"], {
                    "level_ids": level["id"],
                    "include": "permissions:operations(seats:reserve)",
                    "page": 1,
                    "per_page": 150
                }).data,
                self._config.robin_seats_priority
            )

            book_from, book_to = self.__get_book_dates(ZoneInfo(self._config.timezone))

            reservations = api_client.reservations_seats({
                "level_ids": level["id"],
                "after": book_from.isoformat(),
                "before": book_to.isoformat(),
                "page": 1,
                "per_page": 2000
            }).data

            free_seat = self.__get_first_free_seat(seats, reservations)

            if free_seat is None:
                raise ActionError('Free seat for booking is not found')

            api_client.reserve_seat(free_seat["id"], {
                "type": "hoteled",
                "start": {
                    "date_time": book_from.isoformat(),
                    "time_zone": self._config.timezone
                },
                "end": {
                    "date_time": book_to.isoformat(),
                    "time_zone": self._config.timezone
                },
                "reservee": {
                    "user_id": user["id"]
                }
            })

    def __get_sorted_by_priority_seats(self, seats: list[JsonDict], priority: list[str]) -> list[JsonDict]:
        return sorted(seats, key=lambda x: (0, priority.index(x["name"])) if x["name"] in priority else (1, 0))

    def __get_first_free_seat(self, seats: list[JsonDict], reservations: list[JsonDict]) -> Optional[JsonDict]:
        reserved_seats_ids = list(map(lambda x: x["seat_id"], reservations))

        for seat in seats:
            if seat["is_disabled"] \
                    or not seat["is_reservable"] \
                    or not seat["permissions"]["seats:reserve"] \
                    or seat["id"] in reserved_seats_ids:
                continue

            return seat

        return None

    def __get_book_dates(self, tz: ZoneInfo) -> tuple[datetime, datetime]:
        book_date = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=3)
        return (book_date.astimezone(ZoneInfo("UTC")), book_date.replace(hour=20, minute=30).astimezone(ZoneInfo("UTC")))

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
