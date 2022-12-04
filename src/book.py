from selenium import webdriver
import os

ROBIN_DASHBOARD_URL = "https://dashboard.robinpowered.com/"
ROBIN_API_URL = "https://api.robinpowered.com/v1.0"

ROBIN_CREDENTIALS = os.getenv("ROBIN_CREDENTIALS")
ROBIN_ORGANIZATION_ID = os.getenv("ROBIN_ORGANIZATION_ID")
SELENIUM_WEBDRIVER_URL = os.getenv("SELENIUM_WEBDRIVER_URL")

options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Remote(command_executor=SELENIUM_WEBDRIVER_URL, options=options)
try:
    driver.get(ROBIN_DASHBOARD_URL)

    script = """
let callback = arguments[arguments.length - 1];

fetch("{api_url}/auth/users", {{
    "headers": {{
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7",
        "authorization": "Basic {credentials}",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua": "\\"Google Chrome\\";v=\\"107\\", \\"Chromium\\";v=\\"107\\", \\"Not=A?Brand\\";v=\\"24\\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\\"macOS\\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-requested-with": "robin/dashboard"
    }},
    "body": "{{\\"remember_me\\":false,\\"organization\\":{organization}}}",
    "method": "POST"
}})
    .then(r => r.json())
    .then(r => {{ callback(r) }});
""".format(api_url=ROBIN_API_URL,
           credentials=ROBIN_CREDENTIALS,
           organization=ROBIN_ORGANIZATION_ID)

    response = driver.execute_async_script(script=script)

    access_token = response["data"]["access_token"]

    script = """
let callback = arguments[arguments.length - 1];

fetch("{api_url}/me", {{
    "headers": {{
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7",
        "authorization": "Access-Token {access_token}",
        "sec-ch-ua": "\\"Google Chrome\\";v=\\"107\\", \\"Chromium\\";v=\\"107\\", \\"Not=A?Brand\\";v=\\"24\\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\\"macOS\\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "tenant-id": "{organization}",
        "x-requested-with": "robin/dashboard"
    }},
    "body": null,
    "method": "GET"
}})
    .then(r => r.json())
    .then(r => {{ callback(r) }});
""".format(api_url=ROBIN_API_URL,
           access_token=access_token,
           organization=ROBIN_ORGANIZATION_ID)
    
    response = driver.execute_async_script(script=script)

    print(response)
finally:
    driver.quit()
