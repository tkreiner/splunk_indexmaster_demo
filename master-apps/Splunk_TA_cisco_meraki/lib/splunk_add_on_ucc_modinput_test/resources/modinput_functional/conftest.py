#   DO NOT MODIFY CODE IN THIS FILE
from typing import Generator
import pytest
from splunk_add_on_ucc_modinput_test.common.splunk_instance import (
    Configuration as SplunkConfiguration,
)
from tests.modinput_functional.vendor_product import (
    Configuration as VendorProductConfiguration,
)
from tests.modinput_functional.ta import Configuration as TaConfiguration


#   DO NOT MODIFY CODE IN THIS FILE
@pytest.fixture(scope="session")
def configuration() -> Generator[TaConfiguration, None, None]:
    ta_configuration = TaConfiguration(
        splunk_configuration=SplunkConfiguration(),
        vendor_product_configuration=VendorProductConfiguration(),
    )
    ta_configuration.set_up(ta_configuration.api_instance)
    yield ta_configuration
    ta_configuration.tear_down(ta_configuration.api_instance)


#   DO NOT MODIFY CODE IN THIS FILE
