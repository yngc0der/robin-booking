import os
import actions
from argparse import ArgumentParser

def main() -> None:
    parser = ArgumentParser("Robin booking")
    parser.add_argument("action")

    args = parser.parse_args()

    config = actions.Config(
        selenium_webdriver_url=os.getenv("SELENIUM_WEBDRIVER_URL"),
        robin_credentials=os.getenv("ROBIN_CREDENTIALS"),
        robin_seats_priority=os.getenv("ROBIN_SEATS_PRIORITY").split(","),
        robin_organization=os.getenv("ROBIN_ORGANIZATION"),
        robin_location=os.getenv("ROBIN_LOCATION"),
        robin_level=os.getenv("ROBIN_LEVEL"),
        timezone=os.getenv("TZ")
    )

    match args.action:
        case "book":
            action = actions.BookAction(config)
        case "checkin":
            action = actions.CheckinAction(config)
        case _:
            raise NotImplementedError('Action is not exists')

    action.exec()

if __name__ == "__main__":
    main()
