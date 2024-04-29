# mypy: disable-error-code="attr-defined,arg-type"

import time
import pytest
import requests  # type: ignore
from requests.adapters import HTTPAdapter, Retry  # type: ignore
from splunklib import client
from splunklib.client import Service
from splunklib.client import Job
from splunklib.client import Index
import splunklib.results as results
from splunk_add_on_ucc_modinput_test.common import utils


class Configuration:
    @staticmethod
    def get_index(index_name: str, client_service: Service) -> Index:
        if any(i.name == index_name for i in client_service.indexes):
            return client_service.indexes[index_name]
        else:
            return None

    @staticmethod
    def _victoria_create_index(
        index_name: str, *, acs_stack: str, acs_server: str, splunk_token: str
    ) -> None:
        url = f"{acs_server}/{acs_stack}/adminconfig/v2/indexes"
        data = {
            "datatype": "event",
            "maxDataSizeMB": 0,
            "name": index_name,
            "searchableDays": 365,
            "splunkArchivalRetentionDays": 366,
            "totalEventCount": "0",
            "totalRawSizeMB": "0",
        }
        headers = {
            "Authorization": "Bearer " + splunk_token,
            "Content-Type": "application/json",
        }
        idx_not_created_msg = f"Index {index_name} was not created on stack \
            {acs_stack} controlleb by {acs_server}"
        response = requests.post(url, headers=headers, json=data)
        if response.ok:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[404])
            session.mount("http://", HTTPAdapter(max_retries=retries))
            response = session.get(f"{url}/{index_name}", headers=headers)
            if response.ok:
                return
            else:
                idx_not_created_msg += " or creation time exceeded timeout"
        utils.logger.critical(idx_not_created_msg)
        pytest.exit(idx_not_created_msg)

    @staticmethod
    def _enterprise_create_index(
        index_name: str, client_service: Service
    ) -> Index:
        idx_not_created_msg = f"Index {index_name} was not created on \
            instance {client_service.host}"
        try:
            new_index = client_service.indexes.create(index_name)
        except Exception as e:
            reason = f"{idx_not_created_msg}\nException raised:\n{e}"
            utils.logger.critical(reason)
            pytest.exit(reason)
        if new_index:
            return new_index
        else:
            utils.logger.critical(idx_not_created_msg)
            pytest.exit(idx_not_created_msg)

    __instance = None

    def __new__(cls, *args, **kwargs):  # type: ignore
        if not Configuration.__instance:
            Configuration.__instance = object.__new__(cls)
            Configuration.__instance._host = (
                utils.get_from_environment_variable(
                    "MODINPUT_TEST_SPLUNK_HOST"
                )
            )
            Configuration.__instance._port = (
                utils.get_from_environment_variable(
                    "MODINPUT_TEST_SPLUNK_PORT"
                )
            )
            Configuration.__instance._username = (
                utils.get_from_environment_variable(
                    "MODINPUT_TEST_SPLUNK_USERNAME"
                )
            )
            Configuration.__instance._password = (
                utils.get_from_environment_variable(
                    "MODINPUT_TEST_SPLUNK_PASSWORD_BASE64",
                    string_function=utils.Base64.decode,
                )
            )
            dedicated_index_name = utils.get_from_environment_variable(
                "MODINPUT_TEST_SPLUNK_DEDICATED_INDEX",
                is_optional=True,
            )
            Configuration.__instance._is_cloud = (
                "splunkcloud.com"
                in Configuration.__instance._host.lower()  # type: ignore
            )
            create_index_in_cloud = (
                Configuration.__instance._is_cloud and not dedicated_index_name
            )
            Configuration.__instance._token = (
                utils.get_from_environment_variable(
                    "MODINPUT_TEST_SPLUNK_TOKEN_BASE64",
                    string_function=utils.Base64.decode,
                    is_optional=not create_index_in_cloud,
                )
            )
            Configuration.__instance._acs_server = (
                utils.get_from_environment_variable(
                    "MODINPUT_TEST_ACS_SERVER",
                    is_optional=not create_index_in_cloud,
                )
            )
            Configuration.__instance._acs_stack = (
                utils.get_from_environment_variable(
                    "MODINPUT_TEST_ACS_STACK",
                    is_optional=not create_index_in_cloud,
                )
            )
            Configuration.__instance._service = client.connect(
                host=Configuration.__instance._host,
                port=Configuration.__instance._port,
                username=Configuration.__instance._username,
                password=Configuration.__instance._password,
            )

            if dedicated_index_name:
                Configuration.__instance._dedicated_index = (
                    Configuration.get_index(
                        dedicated_index_name, Configuration.__instance._service
                    )
                )
                if not Configuration.__instance._dedicated_index:
                    reason = f"Environment variable \
                        MODINPUT_TEST_SPLUNK_DEDICATED_INDEX set to \
                            {dedicated_index_name}, but Splunk instance \
                                {Configuration.__instance._host} does not \
                                    contain such index. Remove the variable \
                                        or create the index."
                    utils.logger.critical(reason)
                    pytest.exit(reason)
                utils.logger.debug(
                    f"Existing index {dedicated_index_name} will be used for \
                        test in splunk {Configuration.__instance._host}"
                )
            else:
                created_index_name = f"idx_{utils.Common().sufix}"
                if Configuration.get_index(
                    created_index_name, Configuration.__instance._service
                ):
                    reason = f"Index {created_index_name} already exists"
                    utils.logger.critical(reason)
                    pytest.exit(reason)
                if create_index_in_cloud:
                    Configuration._victoria_create_index(
                        created_index_name,
                        acs_stack=Configuration.__instance._acs_stack,
                        acs_server=Configuration.__instance._acs_server,
                        splunk_token=Configuration.__instance._token,
                    )
                    Configuration.__instance._dedicated_index = (
                        Configuration.get_index(
                            created_index_name,
                            Configuration.__instance._service,
                        )
                    )
                else:
                    Configuration.__instance._dedicated_index = (
                        Configuration._enterprise_create_index(
                            created_index_name,
                            Configuration.__instance._service,
                        )
                    )
                utils.logger.debug(
                    f"Index {created_index_name} has just been created in \
                        splunk {Configuration.__instance._host}"
                )

            utils.logger.info(
                f"Splunk - host:port and user set to \
                    {Configuration.__instance._host}:\
                        {Configuration.__instance._port}, \
                            {Configuration.__instance._username}"
            )
            utils.logger.info(
                f"Splunk - index \
                    {Configuration.__instance._dedicated_index.name} will be \
                        used for the test run"
            )
        return Configuration.__instance

    def __init__(self) -> None:
        pass

    @property
    def host(self) -> str:
        return self._host

    @property
    def is_cloud(self) -> bool:
        return self._is_cloud

    @property
    def port(self) -> int:
        return self._port

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def token(self) -> str:
        return self._token

    @property
    def acs_server(self) -> str:
        return (
            self._acs_server
            if self._acs_server or not self.is_cloud
            else "https://admin.splunk.com"
        )

    @property
    def service(self) -> Service:
        return self._service

    @property
    def dedicated_index(self) -> Index:
        return self._dedicated_index


class SearchState:
    def __init__(self, job: Job):
        self._is_done = job["isDone"] == "1"
        self._done_progress = float(job["doneProgress"]) * 100
        self._scan_count = int(job["scanCount"])
        self._event_count = int(job["eventCount"])
        self._result_count = int(job["resultCount"])
        self._results = (
            [
                result
                for result in results.JSONResultsReader(
                    job.results(output_mode="json")
                )
            ]
            if self._is_done
            else None
        )

    @property
    def result_count(self) -> int:
        return self._result_count


def search(*, service: Service, searchquery: str) -> SearchState:
    search_state = None
    kwargs_normalsearch = {"exec_mode": "normal"}
    job = service.jobs.create(searchquery, **kwargs_normalsearch)
    while True:
        while not job.is_ready():
            pass
        if job["isDone"] == "1":
            search_state = SearchState(job)
            break
        time.sleep(1)
    job.cancel()
    return search_state
