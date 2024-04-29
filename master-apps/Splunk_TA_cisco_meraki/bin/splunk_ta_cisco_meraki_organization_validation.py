#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#

"""
This module validates organization being saved by the user
"""

import import_declare_test  # noqa: F401 # isort: skip

import traceback

import cisco_meraki_utils as utils
from splunktaucclib.rest_handler.error import RestError


def organization_validation(region, organization_id, organization_api_key, session_key):
    """
    This method verifies the credentials by making an API call
    """
    logger = utils.set_logger(
        session_key, "splunk_ta_cisco_meraki_organization_validation"
    )
    logger.info(
        "Verifying API key for the organization id {} ({} region)".format(
            organization_id, region
        )
    )
    if not organization_id or not organization_api_key:
        raise RestError(
            400,
            "Provide all necessary arguments: "
            "organization_id and organization_api_key.",
        )
    try:
        proxy_settings = utils.get_proxy_settings(logger, session_key)

        dashboard = utils.build_dashboard_api(
            region, organization_api_key, proxy_settings
        )
        organizations = dashboard.organizations.getOrganizations()
        valid_organization_id = False
        for organization in organizations:
            if str(organization["id"]) == str(organization_id):
                valid_organization_id = True
                break
        if not valid_organization_id:
            msg = "Failed to validate organization id: {} ({} region)".format(
                organization_id, region
            )
            logger.error(msg)
            raise RestError(400, msg)
    except Exception:
        logger.error(
            "Failed to connect to Meraki for organization id: {} ({} region). {}".format(
                organization_id, region, traceback.format_exc()
            )
        )
        msg = (
            "Could not connect to Meraki for organization id: {} ({} region). "
            "Check configuration and network settings".format(organization_id, region)
        )
        raise RestError(400, msg)
