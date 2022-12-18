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
        robin_user_id=int(os.getenv("ROBIN_USER_ID")),
        robin_organization_id=int(os.getenv("ROBIN_ORGANIZATION_ID")),
        robin_space_id=int(os.getenv("ROBIN_SPACE_ID")),
        robin_level_id=int(os.getenv("ROBIN_LEVEL_ID")),
        robin_seats_priority=os.getenv("ROBIN_SEATS_PRIORITY").split(","),
        timezone=os.getenv("TZ")
    )

    match args.action:
        case "book":
            action = actions.BookAction(config)
        case _:
            raise NotImplementedError('Action is not exists')

    action.exec()

if __name__ == "__main__":
    main()
