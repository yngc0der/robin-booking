from robin import ApiClient, JsonDict
from robin.http import HttpClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
import os

SELENIUM_WEBDRIVER_URL = os.getenv("SELENIUM_WEBDRIVER_URL")
ROBIN_CREDENTIALS = os.getenv("ROBIN_CREDENTIALS")
ROBIN_USER_ID = int(os.getenv("ROBIN_USER_ID"))
ROBIN_ORGANIZATION_ID = int(os.getenv("ROBIN_ORGANIZATION_ID"))
ROBIN_SPACE_ID = int(os.getenv("ROBIN_SPACE_ID"))
ROBIN_LEVEL_ID = int(os.getenv("ROBIN_LEVEL_ID"))
ROBIN_SEATS_PRIORITY = os.getenv("ROBIN_SEATS_PRIORITY").split(",")
TIMEZONE = os.getenv("TZ")

def get_sorted_by_priority_seats(seats: list[JsonDict], priority: list[str]) -> list[JsonDict]:
    return sorted(seats, key=lambda x: (0, priority.index(x["name"])) if x["name"] in priority else (1, 0))

def get_first_free_seat(seats: list[JsonDict], reservations: list[JsonDict]) -> Optional[JsonDict]:
    reserved_seats_ids = list(map(lambda x: x["seat_id"], reservations))

    for seat in seats:
        if seat["is_disabled"] \
                or not seat["is_reservable"] \
                or not seat["permissions"]["seats:reserve"] \
                or seat["id"] in reserved_seats_ids:
            continue

        return seat

    return None

def get_book_dates(tz: ZoneInfo) -> tuple[datetime, datetime]:
    book_date = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=3)
    return (book_date.astimezone(ZoneInfo("UTC")), book_date.replace(hour=20, minute=30).astimezone(ZoneInfo("UTC")))

if __name__ == "__main__":
    with HttpClient.create_webdriver(SELENIUM_WEBDRIVER_URL) as driver:
        api_client = ApiClient(HttpClient(driver))

        api_client.authenticate(ROBIN_CREDENTIALS, ROBIN_ORGANIZATION_ID)

        seats_response = api_client.space_seats(ROBIN_SPACE_ID, {
            "include": "permissions:operations(seats:reserve)",
            "page": 1,
            "per_page": 100
        })

        seats = get_sorted_by_priority_seats(seats_response.data, ROBIN_SEATS_PRIORITY)

        book_from, book_to = get_book_dates(ZoneInfo(TIMEZONE))

        reservations_response = api_client.reservations_seats({
            "level_ids": ROBIN_LEVEL_ID,
            "after": book_from.isoformat(),
            "before": book_to.isoformat(),
            "page": 1,
            "per_page": 2000
        })

        reservations = reservations_response.data

        free_seat = get_first_free_seat(seats, reservations)

        if free_seat is None:
            print('Free seat for booking is not found')
            exit(1)

        reserve_seat_response = api_client.reserve_seat(free_seat["id"], {
            "type": "hoteled",
            "start": {
                "date_time": book_from.isoformat(),
                "time_zone": TIMEZONE
            },
            "end": {
                "date_time": book_to.isoformat(),
                "time_zone": TIMEZONE
            },
            "reservee": {
                "user_id": 965810
            }
        })

        print('Seat has been booked')
