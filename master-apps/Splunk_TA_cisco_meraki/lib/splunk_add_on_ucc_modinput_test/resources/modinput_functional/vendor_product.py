import json
from typing import Optional
import requests  # type: ignore
from requests.auth import HTTPBasicAuth  # type: ignore
from splunk_add_on_ucc_modinput_test.common import utils

#   BE AWARE
#   the file content is extremely vendor product specific
#   to be consistent with framework, you just need to keep Configuration class
#   it is also adviced to have unique events creation in dedicated functions


class Configuration:
    def __init__(self) -> None:
        self._domain = utils.get_from_environment_variable(
            "MODINPUT_TEST_FOOBAR_DOMAIN"
        )
        self._username = utils.get_from_environment_variable(
            "MODINPUT_TEST_FOOBAR_USERNAME"
        )
        self._token = utils.get_from_environment_variable(
            "MODINPUT_TEST_FOOBAR_TOKEN_BASE64",
            string_function=utils.Base64.decode,
        )

    @property
    def domain(self) -> Optional[str]:
        return self._domain

    @property
    def username(self) -> Optional[str]:
        return self._username

    @property
    def token(self) -> Optional[str]:
        return self._token

    @property
    def url(self) -> str:
        return f"https://{self.domain}.foo.bar/rest/api/2/group"

    @property
    def auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(
            self.username,
            self.token,
        )


def _get_group_name() -> str:
    return f"g_{utils.Common().sufix}"


def group_create(configuration: Configuration) -> str:
    _GROUP_NAME = _get_group_name
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"name": _GROUP_NAME})

    try:
        response = requests.request(
            "POST",
            configuration.url,
            data=payload,
            headers=headers,
            auth=configuration.auth,
        )
    except Exception as e:
        msg = (
            f"Error occured during Foo Bar group {_GROUP_NAME} creation:\n{e}"
        )
        utils.logger.error(msg)
        pytest.exit(1, msg=msg)  # type: ignore # noqa: F821
    response_json = json.loads(response.text)
    utils.logger.debug(
        json.dumps(
            response_json, sort_keys=True, indent=4, separators=(",", ": ")
        )
    )
    groupId = response_json["groupId"]

    return groupId


def group_delete(configuration: Configuration) -> None:
    _GROUP_NAME = _get_group_name
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"name": _GROUP_NAME})

    try:
        response = requests.request(
            "GET",
            configuration.url,
            data=payload,
            headers=headers,
            auth=configuration.auth,
        )
    except Exception as e:
        msg = (
            f"Error occured during Foo Bar group {_GROUP_NAME} creation:\n{e}"
        )
        utils.logger.error(msg)
        pytest.exit(1, msg=msg)  # type: ignore # noqa: F821
    response_json = json.loads(response.text)
    utils.logger.debug(
        json.dumps(
            response_json, sort_keys=True, indent=4, separators=(",", ": ")
        )
    )
    groupId = response_json["groupId"]

    query = {"groupId": f"{groupId}"}
    try:
        response = requests.request(
            "DELETE", configuration.url, params=query, auth=configuration.auth
        )
    except Exception as e:
        msg = f"Error occured during Foo Bar group {_GROUP_NAME} deletion \
            (groupId: {groupId}):\n{e}"
        utils.logger.error(msg)
        pytest.exit(1, msg=msg)  # type: ignore # noqa: F821
    utils.logger.debug(response.text)
