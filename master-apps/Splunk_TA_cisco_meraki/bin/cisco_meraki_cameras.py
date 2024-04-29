#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#

import import_declare_test  # noqa: F401 # isort: skip

import sys

import cisco_meraki_base_script as base_script
import cisco_meraki_utils as utils
from splunklib import modularinput as smi


class Cameras(base_script.BaseScript):
    def __init__(self):
        super(Cameras, self).__init__()
        self.logfile_prefix = "splunk_ta_cisco_meraki_cameras"
        self.sourcetype = utils.CAMERAS_SOURCETYPE

    def get_scheme(self):
        scheme = smi.Scheme("cameras")
        scheme.description = "Cameras"
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True
        scheme.use_single_instance = False

        scheme.add_argument(
            smi.Argument(
                "name", title="Name", description="Name", required_on_create=True
            )
        )

        return scheme


if __name__ == "__main__":
    exit_code = Cameras().run(sys.argv)
    sys.exit(exit_code)
