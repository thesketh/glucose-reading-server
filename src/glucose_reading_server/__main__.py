"""Command line app to launch the glucose reading server."""
from argparse import ArgumentParser
import os

import uvicorn  # type: ignore

from .app import APP
from .dependencies import set_reading_store_engine, set_test_reading_store


def main():
    """
    The main entrypoint, which runs the glucose reading server with options
    supplied from command line args.

    """
    parser = ArgumentParser(
        prog="glucose_reading_server", description="A server to track glucose readings."
    )
    parser.add_argument(
        "--port", "-p", type=int, help="the port to run the server on", default=8000
    )
    parser.add_argument(
        "--address", "-a", help="the address to run the server on", default="127.0.0.1"
    )
    parser.add_argument(
        "--connection-string",
        "-c",
        type=str,
        help=(
            "the SQLAlchemy connection string. This can also be set as an environment"
            + "variable ('GLUC_STORE_CONN_STR')"
        ),
        default=None,
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help=(
            "run in test mode. This will store readings in a Python dict instead of "
            + "a database and will not persist them between sessions"
        ),
    )

    args = parser.parse_args()

    if args.test_mode:
        set_test_reading_store()
    else:
        connection_string = args.connection_string or os.getenv("GLUC_STORE_CONN_STR")
        if connection_string is None:
            raise ValueError(
                "Error getting glucose data store. Set 'GLUC_STORE_CONN_STR' env var "
                + "to SQLAlchemy connection string or specify '--connection-string' "
                + "CLI arg"
            )
        set_reading_store_engine(connection_string)

    uvicorn.run(APP, host=args.address, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
