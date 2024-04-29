#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#

import import_declare_test  # noqa: F401 # isort: skip

import logging

from splunk_ta_cisco_meraki_organization_validation import organization_validation
from splunktaucclib.rest_handler import admin_external, util
from splunktaucclib.rest_handler.admin_external import AdminExternalHandler
from splunktaucclib.rest_handler.endpoint import (
    RestModel,
    SingleModel,
    field,
    validator,
)

util.remove_http_proxy_env_vars()


fields = [
    field.RestField(
        "region",
        required=True,
        encrypted=False,
        default=None,
        validator=validator.Enum(
            values={"global", "china"},
        ),
    ),
    field.RestField(
        "organization_id",
        required=True,
        encrypted=False,
        default=None,
        validator=validator.AllOf(
            validator.String(
                max_len=50,
                min_len=1,
            ),
            validator.Pattern(
                regex=r"""^\d+$""",
            ),
        ),
    ),
    field.RestField(
        "organization_api_key",
        required=True,
        encrypted=True,
        default=None,
        validator=validator.AllOf(
            validator.String(
                max_len=50,
                min_len=1,
            ),
            validator.Pattern(
                regex=r"""^[a-z0-9]+$""",
            ),
        ),
    ),
]
model = RestModel(fields, name=None)


endpoint = SingleModel(
    "splunk_ta_cisco_meraki_organization", model, config_name="organization"
)


class CiscoMerakiOrganizationExternalHandler(AdminExternalHandler):
    def __init__(self, *args, **kwargs):
        AdminExternalHandler.__init__(self, *args, **kwargs)

    def handleList(self, confInfo):
        AdminExternalHandler.handleList(self, confInfo)

    def handleEdit(self, confInfo):
        organization_validation(
            self.payload.get("region"),
            self.payload.get("organization_id"),
            self.payload.get("organization_api_key"),
            self.getSessionKey(),
        )
        AdminExternalHandler.handleEdit(self, confInfo)

    def handleCreate(self, confInfo):
        organization_validation(
            self.payload.get("region"),
            self.payload.get("organization_id"),
            self.payload.get("organization_api_key"),
            self.getSessionKey(),
        )
        AdminExternalHandler.handleCreate(self, confInfo)

    def handleRemove(self, confInfo):
        AdminExternalHandler.handleRemove(self, confInfo)


if __name__ == "__main__":
    logging.getLogger().addHandler(logging.NullHandler())
    admin_external.handle(
        endpoint,
        handler=CiscoMerakiOrganizationExternalHandler,
    )
