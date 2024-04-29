# mypy: disable-error-code="attr-defined"

from splunk_add_on_ucc_modinput_test.common.splunk_instance import (
    Configuration as SplunkConfiguration,
)
from tests.modinput_functional.vendor_product import (
    Configuration as VendorProductConfiguration,
)
from splunk_add_on_ucc_modinput_test.common import utils
from splunk_add_on_ucc_modinput_test.common.ta_base import (
    ConfigurationBase,
    InputConfigurationBase,
)
from swagger_client import DefaultApi
from swagger_client.rest import ApiException

output_mode = "json"
pprint = utils.logger.debug
print = utils.logger.error

NAME = "splunk_ta_foo_bar"  # will be replaced by ucc-test-modinput init


# create modinput type specific classes
# InputTypeAbcConfiguration and InputTypeXyzConfiguration are just examples
# and should be used as motivation for your code
# Remember to remove the example code once you are done with your
# customizations
class InputTypeAbcConfiguration(InputConfigurationBase):
    # kwarguments (the one following *) are TA specific
    # and should be a subject of customization
    # you may want to customize list of positional arguments (before *),
    # if you want to customize default interval
    def __init__(
        self,
        name_prefix: str,
        *,
        token_name: str,
        from_timestamp: str,
    ):
        super().__init__(name_prefix=name_prefix)
        # kwarguments assignment is TA specific
        self.token_name = token_name
        self.from_timestamp = from_timestamp


class InputTypeXyzConfiguration(InputConfigurationBase):
    def __init__(
        self,
        name_prefix: str,
        interval: int = 86400,
    ):
        super().__init__(name_prefix=name_prefix, interval=interval)


#   do not modify the code below
class Configuration(ConfigurationBase):
    def __init__(
        self,
        *,
        splunk_configuration: SplunkConfiguration,
        vendor_product_configuration: VendorProductConfiguration,
    ):
        super().__init__(
            splunk_configuration=splunk_configuration,
            vendor_product_configuration=vendor_product_configuration,
        )
        #   do not modify the code above

        # variables that are defined in TA Configuration (as token)
        # may be needed in setup and teardown operations
        # so are assigned to Configuration object
        self.token_name = f"tkn_{utils.Common().sufix}"
        #   while other are Inputs specific so stay private for __init__ method
        from_timestamp = utils.convert_to_utc(
            utils.Common().start_timestamp, format="%Y-%m-%dT%H:%M:%S"
        )

        #   add input configuration to inputs list
        self.add_input_configuration(
            InputTypeAbcConfiguration(
                name_prefix="in_",
                token_name=self.token_name,
                from_timestamp=from_timestamp,
            )
        )
        self.add_input_configuration(
            InputTypeXyzConfiguration(
                name_prefix="daily_in_",
            )
        )

    #   BE AWARE
    #   set_up and tear_down methods are required by the framework
    def set_up(self, api_instance: DefaultApi) -> None:
        #   keep setting loglevel to DEBUG as a good practice
        try:
            api_response = (
                api_instance.splunk_ta_foo_bar_settings_logging_post(
                    output_mode=output_mode, loglevel="DEBUG"
                )
            )
            pprint(api_response)
        except ApiException as e:
            print(
                "Exception when calling \
                    DefaultApi->splunk_ta_foo_bar_settings_logging_post: %s\n"
                % e
            )

        # create vendor product specific configuration
        # you can get current configuration, just for evidence
        try:
            api_response = api_instance.splunk_ta_foo_bar_domain_get(
                output_mode=output_mode
            )
            pprint(api_response)
        except ApiException as e:
            print(
                "Exception when calling \
                    DefaultApi->splunk_ta_foo_bar_domain_get: %s\n"
                % e
            )
        # and add your value
        try:
            api_response = api_instance.splunk_ta_foo_bar_domain_post(
                output_mode=output_mode,
                name=self.vendor_product_configuration.domain,
            )
            pprint(api_response)
        except ApiException as e:
            print(
                "Exception when calling \
                    DefaultApi->splunk_ta_foo_bar_domain_post: %s\n"
                % e
            )

        try:
            api_response = api_instance.splunk_ta_foo_bar_api_token_post(
                output_mode=output_mode,
                domain=self.vendor_product_configuration.domain,
                name=self.token_name,
                username=self.vendor_product_configuration.username,
                token=self.vendor_product_configuration.token,
            )
            pprint(api_response)
        except ApiException as e:
            print(
                "Exception when calling \
                    DefaultApi->splunk_ta_foo_bar_api_token_name_post: %s\n"
                % e
            )

        #   create all inputs
        for input_configuration in self.get_all_inputs():
            if isinstance(input_configuration, InputTypeAbcConfiguration):
                try:
                    api_response = (
                        api_instance.splunk_ta_foo_bar_abc_input_post(
                            output_mode=output_mode,
                            api_token=input_configuration.token_name,
                            name=input_configuration.name,
                            _from=input_configuration.from_timestamp,
                            interval=input_configuration.interval,
                            index=input_configuration.index,
                        )
                    )
                    pprint(api_response)
                except ApiException as e:
                    print(
                        "Exception when calling \
                            DefaultApi->splunk_ta_foo_bar_abc_input_post:\
                                %s\n"
                        % e
                    )
            elif isinstance(input_configuration, InputTypeXyzConfiguration):
                try:
                    api_response = (
                        api_instance.splunk_ta_foo_bar_xyz_input_post(
                            output_mode=output_mode,
                            name=input_configuration.name,
                            interval=input_configuration.interval,
                            index=input_configuration.index,
                        )
                    )
                    pprint(api_response)
                except ApiException as e:
                    print(
                        "Exception when calling \
                            DefaultApi->splunk_ta_foo_bar_xyz_input_post:\
                                %s\n"
                        % e
                    )

    #   BE AWARE
    #   set_up and tear_down methods are required by the framework
    def tear_down(self, api_instance: DefaultApi) -> None:
        #   disable all inputs
        for input_configuration in self.get_all_inputs():
            if isinstance(input_configuration, InputTypeAbcConfiguration):
                try:
                    api_response = (
                        api_instance.splunk_ta_foo_bar_abc_input_name_post(
                            output_mode=output_mode,
                            name=input_configuration.name,
                            disabled=True,
                        )
                    )
                    pprint(api_response)
                except ApiException as e:
                    print(
                        "Exception when calling \
                            DefaultApi->splunk_ta_foo_bar_abc_input_name_post:\
                                %s\n"
                        % e
                    )
            elif isinstance(input_configuration, InputTypeXyzConfiguration):
                try:
                    api_response = (
                        api_instance.splunk_ta_foo_bar_xyz_input_name_post(
                            output_mode=output_mode,
                            name=input_configuration.name,
                            disabled=True,
                        )
                    )
                    pprint(api_response)
                except ApiException as e:
                    print(
                        "Exception when calling \
                            DefaultApi->splunk_ta_foo_bar_xyz_input_name_post:\
                                 %s\n"
                        % e
                    )
