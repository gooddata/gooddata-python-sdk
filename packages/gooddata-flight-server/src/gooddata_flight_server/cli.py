#  (C) 2024 GoodData Corporation
import argparse
import sys
import traceback
from typing import Optional, TypeVar

from dynaconf import ValidationError

from gooddata_flight_server.exceptions import FlightMethodsModuleError, ServerStartupInterrupted
from gooddata_flight_server.server.server_base import DEFAULT_LOGGING_INI
from gooddata_flight_server.server.server_main import GoodDataFlightServer, create_server
from gooddata_flight_server.utils.methods_discovery import get_methods_factory

TConfig = TypeVar("TConfig")


def _add_start_cmd(parser: argparse.ArgumentParser) -> None:
    subcommands = parser.add_subparsers()
    start_cmd = subcommands.add_parser("start")

    start_cmd.add_argument(
        "--methods-provider",
        type=str,
        metavar="METHODS_PROVIDER",
        help="Name of the module providing the server methods. The module must contain a function that implements "
        "the `FlightServerMethodsFactory` protocol and is annotated with the @flight_server_methods decorator. "
        "This class will be used to create the server methods.",
    )
    start_cmd.add_argument(
        "--config",
        type=str,
        nargs="*",
        metavar="CONFIG_FILE",
        help="Optionally specify one or more setting files to use. If not specified, all configuration has to be "
        "provided using environment variables. Important: if you only specify this optional argument, "
        "you must use the `--config-end` to explicitly terminate the list of files - otherwise the CLI cannot "
        "correctly distinguish the end of list and will fail with usage error.",
    )
    start_cmd.add_argument(
        "--config-end",
        action="store_true",
        default=False,
        help="Use this to terminate list of settings files if the --config is the only optional "
        "argument you use in the CLI invocation.",
    )
    start_cmd.add_argument(
        "--logging-config",
        type=str,
        metavar="LOGGING_INI",
        help="File containing configuration of the loggers; if not specified uses configuration where all "
        "loggers are set to info level.",
    )
    start_cmd.add_argument(
        "--dev-log",
        action="store_true",
        default=False,
        required=False,
        help="Render logs in development mode - nicer, formatted and colored output. Not suitable for production due "
        "to both performance impact and not-so-well structured nature. Without this flag, the log output is "
        "produced in JSON format.",
    )

    start_cmd.set_defaults(action="start")


def _create_std_server_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    _add_start_cmd(parser)

    return parser


def _create_server(args: argparse.Namespace) -> GoodDataFlightServer:
    _config_files: tuple[str, ...] = args.config or ()
    config_files = tuple(f for f in _config_files if f is not None)
    methods = get_methods_factory(args.methods_provider)

    return create_server(
        methods=methods,
        config_files=config_files,
        logging_config=args.logging_config or DEFAULT_LOGGING_INI,
        dev_log=args.dev_log or False,
    )


# not really needed to be global, keeping it here so that instance of server is reachable
# easily from the debugger
_SERVER: Optional[GoodDataFlightServer] = None


def server_cli() -> None:
    """
    Sets up argument parsing, validates arguments, read settings using Dynaconf and if
    everything is green calls the provided function.

    :return:
    """
    parser = _create_std_server_argparser()
    args = parser.parse_args()

    if not hasattr(args, "action"):
        parser.print_usage()
        sys.exit(1)

    rc = 0
    try:
        global _SERVER
        _SERVER = _create_server(args=args)
    except ValidationError as e:
        print(f"An error has occurred while reading settings: {str(e)}")
        sys.exit(1)
    except FlightMethodsModuleError as e:
        print(f"An error has occurred while getting the FlightMethodsFactory: {str(e)}")
        sys.exit(1)
    except ServerStartupInterrupted as e:
        print(str(e))
        sys.exit(1)
    except Exception:
        print("An unexpected error has occurred while creating server.")
        traceback.print_exc()
        sys.exit(1)

    try:
        if args.action == "start":
            _SERVER.start()
            _SERVER.wait_for_stop()
            rc = 0 if not _SERVER.aborted() else 1
    except Exception:
        print("An unexpected error has occurred while starting server.")
        traceback.print_exc()
        rc = 1
    finally:
        sys.exit(rc)


if __name__ == "__main__":
    server_cli()
