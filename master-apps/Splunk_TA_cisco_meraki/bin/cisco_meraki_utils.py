#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#

import json
import os.path
import sys
import traceback
import requests
from solnlib import conf_manager, log
from solnlib.modular_input import checkpointer
from splunklib import modularinput as smi

import meraki


SWITCHES_SOURCETYPE = "meraki:switches"
SECURITYAPPLIANCES_SOURCETYPE = "meraki:securityappliances"
ACCESSPOINTS_SOURCETYPE = "meraki:accesspoints"
AIRMARSHAL_SOURCETYPE = "meraki:airmarshal"
CAMERAS_SOURCETYPE = "meraki:cameras"
AUDIT_SOURCETYPE = "meraki:audit"
ORGANIZATIONSECURITY_SOURCETYPE = "meraki:organizationsecurity"

APP_NAME = __file__.split(os.path.sep)[-3]


def build_dashboard_api(region, api_key, proxy):
    """
    Returns Meraki Dashboard API object.
    """
    base_url = (
        "https://api.meraki.cn/api/v1"
        if region == "china"
        else "https://api.meraki.com/api/v1"
    )
    return meraki.DashboardAPI(
        api_key=api_key,
        base_url=base_url,
        output_log=False,
        suppress_logging=True,
        requests_proxy=proxy,
        caller="SplunkAddOnForCiscoMeraki Splunk",
    )


def set_logger(session_key, filename):
    """
    This function sets up a logger with configured log level.
    :param filename: Name of the log file
    :return logger: logger object
    """
    logger = log.Logs().get_logger(filename)
    log_level = conf_manager.get_log_level(
        logger=logger,
        session_key=session_key,
        app_name=APP_NAME,
        conf_name="splunk_ta_cisco_meraki_settings",
        default_log_level="DEBUG",
    )
    logger.setLevel(log_level)
    return logger


def get_proxy_settings(logger, session_key):
    """
    This function reads proxy settings if any, otherwise returns None
    :param session_key: Session key for the particular modular input
    :return: A dictionary proxy having settings
    """
    try:
        settings_cfm = conf_manager.ConfManager(
            session_key,
            APP_NAME,
            realm="__REST_CREDENTIAL__#{}#configs/conf-splunk_ta_cisco_meraki_settings".format(
                APP_NAME
            ),
        )
        splunk_ta_cisco_meraki_settings_conf = settings_cfm.get_conf(
            "splunk_ta_cisco_meraki_settings"
        ).get_all()

        proxy_settings = None
        proxy_stanza = {}
        for k, v in splunk_ta_cisco_meraki_settings_conf["proxy"].items():
            proxy_stanza[k] = v

        if int(proxy_stanza.get("proxy_enabled", 0)) == 0:
            logger.debug("Proxy is disabled. Returning None")
            return proxy_settings
        proxy_type = "http"
        proxy_port = proxy_stanza.get("proxy_port")
        proxy_url = proxy_stanza.get("proxy_url")
        proxy_username = proxy_stanza.get("proxy_username", "")
        proxy_password = proxy_stanza.get("proxy_password", "")

        if proxy_username and proxy_password:
            proxy_username = requests.compat.quote_plus(proxy_username)
            proxy_password = requests.compat.quote_plus(proxy_password)
            proxy_uri = "%s://%s:%s@%s:%s" % (
                proxy_type,
                proxy_username,
                proxy_password,
                proxy_url,
                proxy_port,
            )
        else:
            proxy_uri = "%s://%s:%s" % (proxy_type, proxy_url, proxy_port)
        logger.debug("Successfully fetched configured proxy details.")
        return proxy_uri
    except Exception:
        logger.error(
            "Failed to fetch proxy details from configuration. {}".format(
                traceback.format_exc()
            )
        )
        sys.exit(1)


def get_organization_details(logger, session_key, organization_name):
    """
    This function retrieves organization details from addon configuration file
    :param session_key: Session key for the particular modular input
    :param organization_name: Organization name configured in the addon
    :return: Organization details in form of a dictionary
    """
    try:
        cfm = conf_manager.ConfManager(
            session_key,
            APP_NAME,
            realm="__REST_CREDENTIAL__#{}#configs/conf-splunk_ta_cisco_meraki_organization".format(
                APP_NAME
            ),
        )
        organization_conf_file = cfm.get_conf("splunk_ta_cisco_meraki_organization")
        logger.debug(
            "Reading organization info from splunk_ta_cisco_meraki_organization.conf for organization name {}".format(
                organization_name
            )
        )
        return {
            "region": organization_conf_file.get(organization_name).get("region"),
            "organization_id": organization_conf_file.get(organization_name).get(
                "organization_id"
            ),
            "organization_api_key": organization_conf_file.get(organization_name).get(
                "organization_api_key"
            ),
        }
    except Exception:
        logger.error(
            "Failed to fetch the organization details from splunk_ta_cisco_meraki_organization.conf file "
            + "for the organization '{}': {}".format(
                organization_name, traceback.format_exc()
            )
        )
        sys.exit(
            "Error while fetching organization details. Terminating modular input."
        )


def validate_inputs(input_params):
    """
    This function validates the input parameters.
    :param input_params: dictionary of input parameters
    """
    try:
        interval = int(input_params.get("interval"))
        if interval not in range(360, 3601):
            raise Exception("Interval should be between 360 and 3600 seconds.")
    except ValueError:
        raise Exception(
            "Interval should be an integer and should be in a range from 360 to 3600 seconds"
        )


def validate_inputs_for_audit(input_params):
    """
    This function validates the input parameters for audit input.
    :param input_params: dictionary of input parameters
    """
    validate_inputs(input_params)
    _validate_start_from_days_ago(input_params, range(1, 61))


def validate_inputs_for_airmarshal(input_params):
    """
    This function validates the input parameters for air marshal input.
    :param input_params: dictionary of input parameters
    """
    validate_inputs(input_params)
    _validate_start_from_days_ago(input_params, range(1, 31))


def _validate_start_from_days_ago(input_params, start_from_days_ago_range):
    """
    This function validates the input parameters for start from (days in the past) input.
    :param input_params: dictionary of input parameters
    :param start_from_days_ago_range: range of min and max allowed number of days
    """
    error_msg = (
        f"Start from should be an integer in a range from {start_from_days_ago_range.start}"
        + f" to {(start_from_days_ago_range.stop-1)}"
    )
    try:
        start_from_days_ago_raw = input_params.get("start_from_days_ago")
        if start_from_days_ago_raw is not None:
            start_from_days_ago = int(start_from_days_ago_raw)
            if start_from_days_ago not in start_from_days_ago_range:
                raise Exception(error_msg)
    except ValueError:
        raise Exception(error_msg)


def checkpoint_name_from_input_name(input_name):
    """
    Returns checkpoint name based on the input name.
    :param input_name: Input name
    :return checkpoint_name: Checkpoint name
    """
    return input_name.replace("://", "_")


def checkpoint_handler(logger, session_key, checkpoint_name):
    """
    This function creates as well as handles kv-store checkpoints for each input.
    :param logger: Logger object
    :param session_key: Session key for the particular modular input
    :param checkpoint_name: Name of the checkpoint file for the particular input
    :return checkpoint_exists: True, if checkpoint exists, else False
    :return checkpoint_collection: Checkpoint directory
    """
    try:
        checkpoint_collection = checkpointer.KVStoreCheckpointer(
            checkpoint_name, session_key, APP_NAME
        )
        return True, checkpoint_collection
    except Exception:
        logger.error("Error in Checkpoint handling: {}".format(traceback.format_exc()))
        return False, None


def write_event(logger, event_writer, raw_event, sourcetype, index, source, host):
    """
    This function ingests data into Splunk
    :param logger: Logger instance
    :param event_writer: Event Writer object
    :param raw_event: Raw event to be ingested into Splunk
    :param sourcetype: Sourcetype of the data
    :param index: Index where to write data
    :param source: Source of the data
    :param host: URL which is getting used to fetch events
    :return: boolean value indicating if the event is successfully ingested
    """
    try:
        event = smi.Event(
            data=json.dumps(raw_event),
            sourcetype=sourcetype,
            source=source,
            host=host,
            index=index,
        )
        event_writer.write_event(event)
        return True
    except Exception:
        logger.error("Error writing event to Splunk: {}".format(traceback.format_exc()))
        return False
