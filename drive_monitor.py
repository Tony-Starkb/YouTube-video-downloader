"""
drive_monitor.py — Detects connected drives on Windows
Scans drive letters A–Z and returns all currently active drives,
excluding system drives defined in config.
"""

import os
from typing import Set
from config import EXCLUDED_DRIVES
from logger import logger


def get_active_drives() -> Set[str]:
    """
    Scans all possible Windows drive letters (A–Z) and returns
    a set of drive paths that currently exist on the system.
    Automatically excludes drives listed in EXCLUDED_DRIVES.

    Returns:
        Set[str]: A set of active drive paths e.g. {"D:\\", "E:\\"}
    """
    active_drives: Set[str] = set()

    for ascii_code in range(65, 91):  # A to Z
        drive_letter = chr(ascii_code) + ":\\"
        if os.path.exists(drive_letter) and drive_letter not in EXCLUDED_DRIVES:
            active_drives.add(drive_letter)

    return active_drives


def detect_new_drives(known_drives: Set[str]) -> Set[str]:
    """
    Compares currently active drives against previously known drives
    and returns any newly connected drives.

    Args:
        known_drives (Set[str]): Drives that were active on the last check.

    Returns:
        Set[str]: Newly connected drives since last check.
    """
    current_drives = get_active_drives()
    new_drives = current_drives - known_drives

    if new_drives:
        for drive in new_drives:
            logger.info(f"New drive detected: {drive}")

    return new_drives, current_drives