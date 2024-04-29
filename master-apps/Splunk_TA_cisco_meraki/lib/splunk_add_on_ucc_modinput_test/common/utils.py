# mypy: disable-error-code="attr-defined"

import os
import time
import datetime
from functools import lru_cache
import pytz  # type: ignore
import logging
import base64
import re
from pathlib import Path
from typing import Callable, Optional

global logger


def init_logger() -> logging.Logger:
    """
    Configure file based logger for the plugin
    """
    fh = logging.FileHandler("ucc_modinput_test.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(process)d - %(filename)s - \
            %(funcName)s - %(message)s"
    )
    fh.setFormatter(formatter)
    logger = logging.getLogger("ucc-modinput-test")
    logger.addHandler(fh)
    logging.root.propagate = False
    logger.setLevel(logging.DEBUG)
    return logger


init_logger()
logger = logging.getLogger("ucc-modinput-test")
logger.debug("Logger set")


def get_from_environment_variable(
    environment_variable: str,
    *,
    string_function: Optional[Callable[[str], str]] = None,
    is_optional: bool = False,
) -> Optional[str]:
    def use_string_function_if_needed(
        *, variable: str, function: Callable[[str], str]
    ) -> str:
        return variable if function is None else function(variable)

    if environment_variable not in os.environ and is_optional:
        return None
    if environment_variable not in os.environ:
        logger.critical(40 * "*")
        logger.critical(f"{environment_variable} environment variable not set")
        logger.critical("run below in terminal:")
        logger.critical(f"export {environment_variable}=[your value]")
        logger.critical(40 * "*")
        exit(1)
    return use_string_function_if_needed(
        variable=os.environ[environment_variable],
        function=string_function,  # type: ignore
    )


class Base64:
    @staticmethod
    def _remove_ending_chars(string: str) -> str:
        if len(string) == 0:
            return string
        CHARS_TO_BE_REMOVED = ["\n"]
        for i in range(len(string), -1, -1):
            if string[i - 1] not in CHARS_TO_BE_REMOVED:
                break
        return string[:i]

    @staticmethod
    def encode(string: str) -> str:
        _bytes = Base64._remove_ending_chars(string=string).encode("utf-8")
        base64_encoded = base64.b64encode(_bytes)
        base64_string = base64_encoded.decode("utf-8")
        return base64_string

    @staticmethod
    def decode(base64_string: str) -> str:
        base64_bytes = base64_string.encode("utf-8")
        decoded_bytes = base64.b64decode(base64_bytes)
        string = decoded_bytes.decode("utf-8")
        return Base64._remove_ending_chars(string=string)


def get_epoch_timestamp() -> float:
    return time.time()


@lru_cache(maxsize=32)
def convert_to_utc(
    epoch_timestamp: float, format: str = "%Y%m%d%H%M%S"
) -> str:
    return datetime.datetime.fromtimestamp(
        epoch_timestamp, pytz.timezone("UTC")
    ).strftime(format)


class Common:
    __instance = None

    def __new__(cls, *args, **kwargs):  # type: ignore
        if not Common.__instance:
            Common.__instance = object.__new__(cls)
            Common.__instance._start_timestamp = get_epoch_timestamp()
            logger.info(
                f"Test timestamp set to: \
                    {convert_to_utc(Common.__instance._start_timestamp)}"
            )
        return Common.__instance

    def __init__(self) -> None:
        pass

    @property
    def start_timestamp(self) -> float:
        return self._start_timestamp

    @property
    def sufix(self) -> str:
        return f"mit_{convert_to_utc(self.start_timestamp)}"
        # MIT from "MODULARINPUT TEST"


def replace_line(
    *,
    file: Path,
    pattern: str,
    replacement: str,
) -> None:
    logger.debug(
        f"replace_line(file_path:{file},pattern:{pattern},replacement\
            {replacement})"
    )

    with file.open() as f:
        lines = f.readlines()

    found = False
    modified_lines = []
    for line in lines:
        if re.match(pattern, line):
            logger.debug(f"Found a line ({line}) that will be replaced")
            found = True
            line = re.sub(pattern, replacement, line)
        modified_lines.append(line)

    if found:
        with open(file, "w") as f:
            f.writelines(modified_lines)
        logger.debug(
            "Pattern found and replaced successfully. Leaving replace_line."
        )
    else:
        logger.debug("Pattern not found in the file. Leaving replace_line.")
