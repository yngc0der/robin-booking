from actions import AbstractAction
from robin import ApiClient, JsonDict
from robin.http import HttpClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class CheckinAction(AbstractAction):
    def exec(self) -> None:
        with HttpClient.create_webdriver(self._config.selenium_webdriver_url) as driver:
            api_client = ApiClient(HttpClient(driver))

            api_client.authenticate(self._config.robin_credentials, self._config.robin_organization_id)

            checkin_from, checkin_to = self.__get_checkin_dates(ZoneInfo(self._config.timezone))

            reservations_response = api_client.reservations_seats({
                "space_ids": self._config.robin_space_id,
                "level_ids": self._config.robin_level_id,
                "user_ids": self._config.robin_user_id,
                "after": checkin_from.isoformat(),
                "before": checkin_to.isoformat(),
                "page": 1,
                "per_page": 2000
            })

            reservations = reservations_response.data

            for reservation in reservations:
                if reservation["confirmation"] is not None:
                    continue

                api_client.confirm_reservation(reservation["id"], {
                    "user_id": self._config.robin_user_id,
                })

    def __get_checkin_dates(self, tz: ZoneInfo) -> tuple[datetime, datetime]:
        checkin_date = datetime.now(tz).replace(microsecond=0) - timedelta(minutes=30)
        return (checkin_date.astimezone(ZoneInfo("UTC")), (checkin_date + timedelta(hours=1)).astimezone(ZoneInfo("UTC")))
