import json
from selenium import webdriver
from robin.http import Request, Response, RequestError
from robin import JsonDict

class HttpClient:
    def create_webdriver(webdriver_url: str) -> webdriver.remote.webdriver.BaseWebDriver:
        options = webdriver.ChromeOptions()
        options.headless = True
        return webdriver.Remote(command_executor=webdriver_url, options=options)

    def __init__(self, webdriver: webdriver.remote.webdriver.BaseWebDriver) -> None:
        self.__webdriver = webdriver
        self.__webdriver.get("https://dashboard.robinpowered.com/")
        self.__base_url = ""

    def set_base_url(self, url: str) -> None:
        self.__base_url = url

    def send(self, request: Request) -> Response:
        params = self.__make_js_request_params(request)

        script = """
let callback = arguments[arguments.length - 1];

fetch("{base_url}{url}", {params})
    .then(response => response.text().then(body => {{
        let headers = {{}}
        response.headers.forEach((val, key) => {{
            headers[key] = val;
        }});
        return {{
            body,
            headers,
            ok: response.ok,
            redirected: response.redirected,
            status: response.status,
            statusText: response.statusText,
            type: response.type,
            url: response.url,
        }}
    }}))
    .then(data => callback(data))
    .catch(error => callback({{error: error.message}}));
""".format(base_url=self.__base_url, url=request.url, params=json.dumps(params))

        response = self.__webdriver.execute_async_script(script)

        if "error" in response:
            raise RequestError(response["error"])

        return Response(
            body=response["body"],
            headers=response["headers"],
            ok=response["ok"],
            redirected=response["redirected"],
            status=response["status"],
            status_text=response["statusText"],
            type=response["type"],
            url=response["url"]
        )

    def __make_js_request_params(self, request: Request) -> JsonDict:
        params = {}
        params["method"] = request.method
        if request.mode is not None:
            params["mode"] = request.mode
        if request.cache is not None:
            params["cache"] = request.cache
        if request.credentials is not None:
            params["credentials"] = request.credentials
        if request.headers is not None:
            params["headers"] = request.headers
        if request.redirect is not None:
            params["redirect"] = request.redirect
        if request.referrer_policy is not None:
            params["referrerPolicy"] = request.referrer_policy
        if request.body is not None:
            params["body"] = request.body
        return params
