"""
main.py — Entry point for YouTube Auto-Downloader
─────────────────────────────────────────────────
How it works:
  1. System starts and records all currently connected drives.
  2. Monitors for any new drive (pendrive) being plugged in.
  3. On detection → downloads latest videos from configured channels.
  4. Moves downloaded videos to the pendrive.
  5. Returns to monitoring state.

To run:
  python main.py

To configure channels or settings:
  Edit config.py — no other file needs to be touched.
"""

import time
import sys
from drive_monitor import get_active_drives, detect_new_drives
from downloader import download_from_channels
from transfer import transfer_to_pendrive
from config import POLL_INTERVAL_SECONDS
from logger import logger


def run() -> None:
    """
    Main loop — monitors for pendrive insertion and triggers
    the download + transfer pipeline when a new drive is detected.
    """
    logger.info("=" * 50)
    logger.info("  YouTube Auto-Downloader — Started")
    logger.info("=" * 50)

    # Record drives that are already connected at startup
    known_drives = get_active_drives()

    if known_drives:
        logger.info(f"Existing drives found: {', '.join(known_drives)}")
    else:
        logger.info("No external drives currently connected.")

    logger.info("Monitoring for pendrive insertion... (Press Ctrl+C to stop)")
    logger.info("-" * 50)

    try:
        while True:
            new_drives, current_drives = detect_new_drives(known_drives)

            if new_drives:
                pendrive = list(new_drives)[0]
                logger.info(f"Pendrive detected at: {pendrive}")
                logger.info("-" * 50)

                # Step 1 — Download videos from YouTube channels
                download_success = download_from_channels()

                if download_success:
                    # Step 2 — Transfer downloaded videos to pendrive
                    transfer_to_pendrive(pendrive)
                else:
                    logger.error("Download step failed. Skipping transfer.")

                logger.info("-" * 50)
                logger.info("Process complete. Monitoring for next pendrive...")

                # Update known drives so we don't re-trigger on same drive
                known_drives = current_drives.copy()

            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.info("Shutdown requested by user. Exiting cleanly.")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()