#
# Copyright 2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
from pathlib import Path
import shutil
from python_on_whales import docker
from importlib_resources import files
from splunk_add_on_ucc_modinput_test import resources
from splunk_add_on_ucc_modinput_test.common import utils

SWAGGER_CODEGEN_CLI_VERSION = "3.0.46"


def initialize(openapi: Path, modinput: Path) -> Path:
    shutil.copytree(
        str(files(resources).joinpath("modinput_functional")), str(modinput)
    )
    with openapi.open() as f:
        data = json.load(f)
    ta_py_path = modinput / "ta.py"
    utils.replace_line(
        file=ta_py_path,
        pattern=r'NAME = "splunk_ta_foo_bar" #.*',
        replacement=f"NAME = \"{data['info']['title']}\"",
    )
    init_in_tests = modinput.parent / "__init__.py"
    if not init_in_tests.exists():
        init_in_tests.touch()
    return modinput


def generate(
    openapi: Path,
    tmp: Path,
    client: Path,
) -> Path:
    RESTAPI_CLIENT = "restapi_client"
    GENERATOR = "generator"
    restapi_client_path = tmp / RESTAPI_CLIENT
    generator_path = tmp / GENERATOR
    restapi_client_path.mkdir()
    generator_path.mkdir()
    shutil.copy(str(openapi), str(tmp))
    shutil.copy(
        str(
            files(resources).joinpath(
                "swagger-codegen-generators/src/main/resources/handlebars/python/rest.mustache"  # noqa: E501
            )
        ),
        str(generator_path),
    )
    docker.run(
        f"swaggerapi/swagger-codegen-cli-v3:{SWAGGER_CODEGEN_CLI_VERSION}",
        [
            "generate",
            "-i",
            f"/local/{openapi.name}",
            "-l",
            "python",
            "-o",
            f"/local/{RESTAPI_CLIENT}",
            "-t",
            f"/local/{GENERATOR}/",
        ],
        volumes=[(str(tmp.resolve()), "/local")],
        remove=True,
    )
    shutil.copytree(
        str(restapi_client_path / "swagger_client"),
        str(client / "swagger_client"),
    )
    shutil.copy(
        str(restapi_client_path / "README.md"), str(client / "swagger_client")
    )
    return restapi_client_path
