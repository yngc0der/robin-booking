from actions import AbstractAction
from actions.errors import BookError
from robin import ApiClient, JsonDict
from robin.http import HttpClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional

class BookAction(AbstractAction):
    def exec(self) -> None:
        with HttpClient.create_webdriver(self._config.selenium_webdriver_url) as driver:
            api_client = ApiClient(HttpClient(driver))

            api_client.authenticate(self._config.robin_credentials, self._config.robin_organization_id)

            seats_response = api_client.space_seats(self._config.robin_space_id, {
                "level_ids": self._config.robin_level_id,
                "include": "permissions:operations(seats:reserve)",
                "page": 1,
                "per_page": 100
            })

            seats = self.__get_sorted_by_priority_seats(seats_response.data, self._config.robin_seats_priority)

            book_from, book_to = self.__get_book_dates(ZoneInfo(self._config.timezone))

            reservations_response = api_client.reservations_seats({
                "space_ids": self._config.robin_space_id,
                "level_ids": self._config.robin_level_id,
                "after": book_from.isoformat(),
                "before": book_to.isoformat(),
                "page": 1,
                "per_page": 2000
            })

            reservations = reservations_response.data

            free_seat = self.__get_first_free_seat(seats, reservations)

            if free_seat is None:
                raise BookError('Free seat for booking is not found')

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
                    "user_id": self._config.robin_user_id
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
