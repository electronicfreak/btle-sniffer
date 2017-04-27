#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scan for Bluetooth Low Energy packets and attempt to identify them.
"""

import os
import sys
import argparse
import logging
import pathlib

from .sniffer import Sniffer
from ._version import get_versions


REQUIRE_PLATFORM = "linux"
REQUIRE_UID = 0


def main() -> None:
    if sys.platform != REQUIRE_PLATFORM:
        raise RuntimeError("You must run this programme on Linux.")

    if os.geteuid() != REQUIRE_UID:
        raise PermissionError("You must be root to run this programme.")

    parser = argparse.ArgumentParser(
        prog="btlesniffer",
        description="Scan for Bluetooth Low Energy devices and gather information about them."
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="btlesniffer {}".format(get_versions()["version"]),
        help="display version information and exit"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="increase the verbosity of the program"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="enable debugging features"
    )
    parser.add_argument(
        "-o", "--out-path",
        type=str,
        help="path to the device registry backup"
    )
    parser.add_argument(
        "--backup-frequency",
        type=int,
        default=60,
        help="how frequently the device registry backup should be written (in seconds)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="resume from a previous device registry backup (must specify the `-o` option)"
    )
    args = parser.parse_args()

    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2 or args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level)

    if args.out_path is not None:
        backup_path = pathlib.Path(args.out_path)
    else:
        backup_path = None

    with Sniffer(backup_path, args.backup_frequency, 30, args.resume) as sniffer:
        sniffer.run()


if __name__ == "__main__":
    main()
