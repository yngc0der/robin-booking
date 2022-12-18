from robin.http import HttpClient, Request
from robin import ApiResponse, JsonDict, ApiError
from typing import Optional
import json
import urllib.parse

class ApiClient:
    __API_BASE_URL = "https://api.robinpowered.com/v1.0"

    def __init__(self, http_client: HttpClient) -> None:
        self.__http_client = http_client
        self.__http_client.set_base_url(self.__API_BASE_URL)
        self.__access_token = None
    
    def authenticate(self, credentials: str, organization_id: int) -> None:
        response = self.__send_api_request(
            endpoint="/auth/users",
            method="POST",
            body_params={"remember_me": False, "organization": organization_id},
            headers={"authorization": "Basic {}".format(credentials)}
        )

        self.__access_token = response.data["access_token"]

    def seats(self, organization_id: str, params: JsonDict) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/seats",
            method="GET",
            query_params=params,
            headers={
                "authorization": "Access-Token {}".format(self.__access_token),
                "tenant-id": organization_id
            }
        )
        return response

    def space_seats(self, space_id: int, params: JsonDict) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/spaces/{}/seats".format(space_id),
            method="GET",
            query_params=params,
            headers={"authorization": "Access-Token {}".format(self.__access_token)}
        )
        return response

    def reservations_seats(self, params: JsonDict) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/reservations/seats",
            method="GET",
            query_params=params,
            headers={"authorization": "Access-Token {}".format(self.__access_token)}
        )
        return response

    def reserve_seat(self, seat: int, params: JsonDict) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/seats/{}/reservations".format(seat),
            method="POST",
            body_params=params,
            headers={"authorization": "Access-Token {}".format(self.__access_token)}
        )
        return response

    def confirm_reservation(self, reservation_id: str, params: JsonDict) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/reservations/seats/{}/confirmation".format(reservation_id),
            method="PUT",
            body_params=params,
            headers={"authorization": "Access-Token {}".format(self.__access_token)}
        )
        return response

    def organization(self, organization_id: str) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/organizations/{}".format(organization_id),
            method="GET"
        )
        return response

    def locations(self, organization_id: str, params: Optional[JsonDict]) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/organizations/{}/locations".format(organization_id),
            method="GET",
            query_params=params,
            headers={"authorization": "Access-Token {}".format(self.__access_token)}
        )
        return response

    def location_levels(self, location_id: str, params: Optional[JsonDict]) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/locations/{}/levels".format(location_id),
            method="GET",
            query_params=params,
            headers={"authorization": "Access-Token {}".format(self.__access_token)}
        )
        return response

    def me(self) -> ApiResponse:
        response = self.__send_api_request(
            endpoint="/me",
            method="GET",
            headers={"authorization": "Access-Token {}".format(self.__access_token)}
        )
        return response

    def __send_api_request(
        self,
        endpoint: str,
        method: str = "GET",
        query_params: Optional[JsonDict] = None,
        body_params: Optional[JsonDict] = None,
        headers: dict[str, str] = {}
    ) -> ApiResponse:
        url = endpoint
        if query_params is not None and len(query_params) > 0:
            url += "?{}".format(urllib.parse.urlencode(query_params))

        default_headers = {
            "accept": "application/json",
            "content-type": "application/json;charset=UTF-8"
        }
        for name, value in headers.items():
            default_headers[name] = value

        body = json.dumps(body_params) if body_params is not None else None

        response = self.__http_client.send(Request(method, url, headers=default_headers, body=body))

        api_response = ApiResponse.create_from_http_response(response)
        
        if not api_response.is_success:
            raise ApiError("[{}] {}".format(api_response.meta["status"], api_response.meta["message"]))

        return api_response
