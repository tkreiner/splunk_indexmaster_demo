# mypy: disable-error-code="arg-type"

import argparse
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Sequence
from splunk_add_on_ucc_modinput_test import commands, tools


class DefaultSubcommandArgumentParser(argparse.ArgumentParser):
    __default_subparser = None

    def set_default_subparser(self, name: str) -> None:
        self.__default_subparser = name

    def _parse_known_args(self, arg_strings, *args, **kwargs):  # type: ignore
        in_args = set(arg_strings)
        d_sp = self.__default_subparser
        if d_sp is not None and not {"-h", "--help"}.intersection(in_args):
            for x in self._subparsers._actions:  # type: ignore
                subparser_found = isinstance(
                    x, argparse._SubParsersAction
                ) and in_args.intersection(x._name_parser_map.keys())
                if subparser_found:
                    break
            else:
                arg_strings = [d_sp] + arg_strings
        return super()._parse_known_args(arg_strings, *args, **kwargs)


def main(argv: Optional[Sequence[str]] = None) -> int:
    class OpenApiPath:
        DEFAULT = "output/*/appserver/static/openapi.json"

        @staticmethod
        def validate(value: str) -> Path:
            if value != OpenApiPath.DEFAULT:
                p = Path(value)
                if not p.exists():
                    raise argparse.ArgumentTypeError(
                        f"""
                        Given openapi.json path ({value}) does not exist.
                        """
                    )
                return p
            else:
                pl = sorted(Path().glob(OpenApiPath.DEFAULT))
                if len(pl) != 1:
                    raise argparse.ArgumentTypeError(
                        f"""
                        Default path ({OpenApiPath.DEFAULT}) does not work in \
                            this case.
                        It returns {len(pl)} results: {[str(x) for x in pl]}
                        Define path to openapi.json
                        """
                    )
                return pl[0]

    class TmpPath:
        DEFAULT = str(Path(tempfile.gettempdir()) / "modinput")

        @staticmethod
        def validate(value: str) -> Path:
            p = Path(value)
            if p.exists():
                p_resolved = p.resolve()
                target = (
                    p_resolved.parent
                    / "backup"
                    / datetime.now().strftime("%Y%m%d%H%M%S")
                    / p_resolved.name
                )
                target.mkdir(parents=True)
                p.rename(target)
            p.mkdir(parents=True)
            return p

    class ClientCodePath:
        DEFAULT = "."

        @staticmethod
        def validate(value: str) -> Path:
            directory = Path(value)
            if not directory.exists():
                raise argparse.ArgumentTypeError(
                    f"Given directory ({value}) has to exist. Create \
                        {directory.resolve()}"
                )
            return directory

    class ModinputPath:
        DEFAULT = "tests/modinput_functional"

        @staticmethod
        def validate(value: str) -> Path:
            directory = Path(value)
            if directory.exists():
                raise argparse.ArgumentTypeError(
                    f"Given directory ({value}) already exist"
                )
            return directory

    class FilePath:
        @staticmethod
        def validate(value: str) -> Path:
            f = Path(value)
            if not f.exists():
                raise argparse.ArgumentTypeError(f"{value} does not exist")
            elif not f.is_file():
                raise argparse.ArgumentTypeError(f"{value} is not a file")
            return f

    argv = argv if argv is not None else sys.argv[1:]
    parser = DefaultSubcommandArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    gen_parser = subparsers.add_parser(
        "gen", description="Generate python client code from openapi.json"
    )
    init_parser = subparsers.add_parser(
        "init",
        description="Initialize modinput tests. This is one time action.",
    )
    base64encode_parser = subparsers.add_parser(
        "base64encode",
        description="Tool to convert complex string (due to special characters \
            or structure) to base64 string",
    )
    base64decode_parser = subparsers.add_parser(
        "base64decode", description="Tool to decode base64 string"
    )
    parser.set_default_subparser("gen")

    _o_args = (
        "-o",
        "--openapi-json",
    )
    _o_kwargs = {
        "type": OpenApiPath.validate,
        "help": "openapi.json path. Client code will be generated from this.",
        "default": OpenApiPath.DEFAULT,
    }
    gen_parser.add_argument(*_o_args, **_o_kwargs)
    init_parser.add_argument(*_o_args, **_o_kwargs)

    _t_args = (
        "-t",
        "--tmp",
    )
    _t_kwargs = {
        "type": TmpPath.validate,
        "help": "Temporary directory, where resources needed for client code \
            creation will be stored",
        "default": TmpPath.DEFAULT,
    }
    gen_parser.add_argument(*_t_args, **_t_kwargs)
    init_parser.add_argument(*_t_args, **_t_kwargs)

    _c_args = (
        "-c",
        "--client-code",
    )
    _c_kwargs = {
        "type": ClientCodePath.validate,
        "help": "Path to client code directory. This is target directory.",
        "default": ClientCodePath.DEFAULT,
    }
    gen_parser.add_argument(*_c_args, **_c_kwargs)
    init_parser.add_argument(*_c_args, **_c_kwargs)

    init_parser.add_argument(
        "-m",
        "--modinput",
        type=ModinputPath.validate,
        help="Path to modinput_functional. This is target directory.",
        default=ModinputPath.DEFAULT,
    )

    # base64encode_parser.add_argument(
    #     "-f",
    #     "--file",
    #     type=FilePath.validate,
    #     help="Path to input text file.",
    #     required=True
    # )

    base64decode_parser.add_argument(
        "-s",
        "--string",
        type=str,
        help="Base64 encoded string.",
        required=True,
    )

    group = base64encode_parser.add_mutually_exclusive_group()
    group.add_argument(
        "-f",
        "--file",
        type=FilePath.validate,
        help="Path to input text file.",
        # required=True
    )
    group.add_argument(
        "-s",
        "--string",
        type=str,
        help="String to be base64 encoded.",
        # required=True
    )

    args = parser.parse_args(argv)
    if args.command in ["gen", "init"]:
        commands.generate(
            openapi=args.openapi_json,
            tmp=args.tmp,
            client=args.client_code,
        )
    if args.command == "init":
        commands.initialize(
            openapi=args.openapi_json,
            modinput=args.modinput,
        )
    if args.command == "base64encode":
        print(
            tools.base64encode(
                text_file=args.file,
                string=args.string,
            )
        )
    if args.command == "base64decode":
        print(tools.base64decode(base64_string=args.string))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
