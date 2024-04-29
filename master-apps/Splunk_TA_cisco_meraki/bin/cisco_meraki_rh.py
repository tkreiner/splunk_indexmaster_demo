#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#

import os

import splunk.rest as rest
from solnlib import log
from splunktaucclib.rest_handler import admin_external

APP_NAME = __file__.split(os.path.sep)[-3]


class CiscoMerakiExternalHandler(admin_external.AdminExternalHandler):
    """
    This class contains methods related to Checkpointing
    """

    def __init__(self, *args, **kwargs):
        admin_external.AdminExternalHandler.__init__(self, *args, **kwargs)

    def handleList(self, conf_info):
        admin_external.AdminExternalHandler.handleList(self, conf_info)

    def handleEdit(self, conf_info):
        admin_external.AdminExternalHandler.handleEdit(self, conf_info)

    def handleCreate(self, conf_info):
        admin_external.AdminExternalHandler.handleCreate(self, conf_info)

    def handleRemove(self, conf_info):
        self.delete_checkpoint()
        admin_external.AdminExternalHandler.handleRemove(self, conf_info)

    def delete_checkpoint(self):
        """
        Delete the checkpoint when user deletes input
        """
        log_filename = "splunk_ta_cisco_meraki_delete_checkpoint"
        logger = log.Logs().get_logger(log_filename)
        try:
            session_key = self.getSessionKey()
            input_type = self.handler.get_endpoint().input_type
            input_types = [
                "cisco_meraki_audit",
                "cisco_meraki_switches",
                "cisco_meraki_cameras",
                "cisco_meraki_securityappliances",
                "cisco_meraki_organizationsecurity",
                "cisco_meraki_accesspoints",
                "cisco_meraki_airmarshal",
            ]
            if input_type in input_types:
                checkpoint_name = input_type + "_" + str(self.callerArgs.id)
                rest_url = (
                    "/servicesNS/nobody/{}/storage/collections/config/{}/".format(
                        APP_NAME, checkpoint_name
                    )
                )
                _, _ = rest.simpleRequest(
                    rest_url,
                    sessionKey=session_key,
                    method="DELETE",
                    getargs={"output_mode": "json"},
                    raiseAllErrors=True,
                )

                logger.info(
                    "Removed checkpoint for {} input".format(str(self.callerArgs.id))
                )
        except Exception as e:
            logger.error(
                "Error while deleting checkpoint for {} input. Error: {}".format(
                    str(self.callerArgs.id), str(e)
                )
            )
