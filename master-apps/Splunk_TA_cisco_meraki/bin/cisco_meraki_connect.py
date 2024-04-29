#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#

import datetime

import cisco_meraki_utils as utils

# Maps sourcetype to Meraki specific product type.
SOURCETYPE_PRODUCT_TYPE_MAPPING = {
    utils.SWITCHES_SOURCETYPE: "switch",
    utils.SECURITYAPPLIANCES_SOURCETYPE: "appliance",
    utils.ACCESSPOINTS_SOURCETYPE: "wireless",
    utils.CAMERAS_SOURCETYPE: "camera",
}


class MerakiConnect:
    def __init__(self, config):
        """
        Initializes connection to Meraki API.
        :param config: Configuration dictionary
        """
        self.region = config["region"]
        self.organization_id = config["organization_id"]
        self.organization_api_key = config["organization_api_key"]
        self.sourcetype = config["sourcetype"]
        self.index = config["index"]
        self._logger = config["logger"]
        self.proxies = config["proxies"]
        self.input_name = config["input_name"]
        self.session_key = config["session_key"]
        self.start_from_days_ago = config["start_from_days_ago"]
        self.current_time = datetime.datetime.utcnow()
        self.current_time_formatted = self.current_time.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.checkpoint_name = utils.checkpoint_name_from_input_name(self.input_name)
        self.checkpoint_success, self.checkpoint_collection = utils.checkpoint_handler(
            self._logger, self.session_key, self.checkpoint_name
        )
        if self.checkpoint_success:
            self.start_time = self._get_start_time()
        self.dashboard = utils.build_dashboard_api(
            self.region, self.organization_api_key, self.proxies
        )

    def _get_start_time(self):
        checkpoint_data = self.checkpoint_collection.get(self.checkpoint_name)
        if not checkpoint_data:
            self._logger.debug(
                "No checkpoint found for {}".format(self.checkpoint_name)
            )
            if self.start_from_days_ago:
                self._logger.debug(
                    "Found start_from_days_ago for {}".format(self.checkpoint_name)
                )
                start_time = (
                    self.current_time
                    - datetime.timedelta(days=int(self.start_from_days_ago))
                ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                self._logger.debug(
                    "No start_from_days_ago found for {}".format(self.checkpoint_name)
                )
                start_time = (self.current_time - datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                )
        else:
            self._logger.debug("Found checkpoint for {}".format(self.checkpoint_name))
            start_time = checkpoint_data.get("start_time")
        self._logger.info(
            "Start time for checkpoint {} - {}".format(self.checkpoint_name, start_time)
        )
        return start_time

    def get_organization(self):
        """
        Returns organization information for a specific organization.
        """
        self._logger.debug(
            "Getting organization information for {}".format(self.organization_id)
        )
        return self.dashboard.organizations.getOrganization(self.organization_id)

    def get_event_host_from_organization(self, organization_info):
        """
        Returns host derived from organization information.
        """
        url = organization_info["url"]
        return url.split("//")[1].split("/")[0]

    def get_organization_networks(self):
        """
        Returns networks information for a specific organization.
        """
        self._logger.debug(
            "Getting organization networks for {}".format(self.organization_id)
        )
        return self.dashboard.organizations.getOrganizationNetworks(
            self.organization_id,
            perPage=100000,
        )

    def get_organization_configuration_changes(self):
        """
        Returns configuration changes for a specific organization.
        """
        self._logger.debug(
            "Getting organization configuration changes for {}".format(
                self.organization_id
            )
        )
        return self.dashboard.organizations.getOrganizationConfigurationChanges(
            self.organization_id,
            t0=self.start_time,
            total_pages=-1,
        )

    def get_organization_security_events(self):
        """
        Returns security events for a specific organization.
        """
        self._logger.debug(
            "Getting organization appliance security events for {}".format(
                self.organization_id
            )
        )
        return self.dashboard.appliance.getOrganizationApplianceSecurityEvents(
            self.organization_id,
            t0=self.start_time,
            perPage=1000,
            total_pages=-1,
        )

    def get_network_events(self, network_id, product_type):
        """
        Returns network events for a specific product.
        See SOURCETYPE_PRODUCT_TYPE_MAPPING for supported product options.
        """
        self._logger.debug(
            "Getting network events for network {} and product type {}".format(
                network_id, product_type
            )
        )
        return self.dashboard.networks.getNetworkEvents(
            network_id,
            productType=product_type,
            perPage=1000,
            startingAfter=self.start_time,
        )

    def get_airmarshal_events(self, network_id):
        """
        Returns Air Marshal events for specific network.
        """
        self._logger.debug("Getting network events for network {}".format(network_id))
        return self.dashboard.wireless.getNetworkWirelessAirMarshal(
            network_id,
            t0=self.start_time,
        )

    def _collect_events(self):
        """
        Returns all events for a specific sourcetype.
        """
        if self.sourcetype == utils.AUDIT_SOURCETYPE:
            return self.get_organization_configuration_changes()
        if self.sourcetype == utils.ORGANIZATIONSECURITY_SOURCETYPE:
            return self.get_organization_security_events()
        networks = self.get_organization_networks()

        all_events = []
        for network in networks:
            network_id = network["id"]
            if self.sourcetype == utils.AIRMARSHAL_SOURCETYPE:
                try:
                    all_events.extend(self.get_airmarshal_events(network_id))
                except Exception as e:
                    self._logger.error(
                        f"Error while getting air marshal events for network {network_id}: {e}"
                    )
            else:
                product_type = SOURCETYPE_PRODUCT_TYPE_MAPPING[self.sourcetype]
                if product_type in network["productTypes"]:
                    try:
                        events = self.get_network_events(network_id, product_type)
                    except Exception as e:
                        self._logger.error(
                            f"Error while getting network events for network {network_id} and productType "
                            + f"{product_type}: {e}"
                        )
                    for event in events["events"]:
                        all_events.append(event)
        return all_events

    def collect_events(self, event_writer):
        """
        Collects events from Meraki API and writes them to Splunk.
        :param event_writer: Event Writer object
        """
        if not self.checkpoint_success:
            self._logger.info("Could not retrieve checkpoint. Not collecting events.")
            return
        organization_info = self.get_organization()
        host = self.get_event_host_from_organization(organization_info)
        source = self.input_name.replace("://", "::")
        events = self._collect_events()
        self._logger.debug(
            "Collected {} events for input {}".format(len(events), self.input_name)
        )
        for ix in range(len(events) - 1, -1, -1):
            event = events[ix]
            event_written = utils.write_event(
                self._logger,
                event_writer,
                event,
                self.sourcetype,
                self.index,
                source,
                host,
            )
            if not event_written:
                break
            if event.get("occurredAt"):
                event_ts = event["occurredAt"]
            elif event.get("ts"):
                event_ts = event["ts"]
            elif event.get("lastSeen"):
                lastSeen_epoch_time_int = int(event.get("lastSeen"))
                lastSeen_utc_time = datetime.datetime.utcfromtimestamp(
                    lastSeen_epoch_time_int
                )
                event_ts = lastSeen_utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                self._logger.warning(
                    "Could not identify datetime field in event: {}".format(event)
                )
                event_ts = self.current_time_formatted
            checkpoint_data = {
                "start_time": event_ts if ix != 0 else self.current_time_formatted,
            }
            self.checkpoint_collection.update(self.checkpoint_name, checkpoint_data)
