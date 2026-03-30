"""
transfer.py — Handles moving downloaded videos to the pendrive
Safely moves all files from the local download folder to the pendrive,
with error handling for mid-transfer issues like accidental ejection.
"""

import shutil
from pathlib import Path
from config import LOCAL_DOWNLOAD_PATH, PENDRIVE_FOLDER_NAME
from logger import logger


def transfer_to_pendrive(pendrive_path: str) -> bool:
    """
    Moves all downloaded videos from the local laptop folder
    to the connected pendrive.

    - Creates a 'Movies' folder on the pendrive if it doesn't exist.
    - Preserves the folder structure (organized by channel name).
    - Skips individual files that fail without stopping the full transfer.
    - Cleans up the local download folder after successful transfer.

    Args:
        pendrive_path (str): Root path of the connected pendrive e.g. "E:\\"

    Returns:
        bool: True if transfer completed (even partially), False on critical failure.
    """
    source = LOCAL_DOWNLOAD_PATH
    destination = Path(pendrive_path) / PENDRIVE_FOLDER_NAME

    # Check if there is anything to transfer
    all_files = [f for f in source.rglob("*") if f.is_file() and f.name != "downloaded_archive.txt"]

    if not all_files:
        logger.info("No new videos to transfer to pendrive.")
        return True

    logger.info(f"Transferring {len(all_files)} file(s) to {destination}...")

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Could not create destination folder on pendrive: {e}")
        return False

    success_count = 0
    fail_count = 0

    for file in all_files:
        try:
            # Preserve the subfolder structure on the pendrive
            relative_path = file.relative_to(source)
            dest_file = destination / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(file), str(dest_file))
            logger.info(f"Moved: {file.name}")
            success_count += 1

        except FileNotFoundError:
            logger.warning(f"Pendrive may have been ejected. Stopping transfer.")
            break

        except PermissionError:
            logger.warning(f"Permission denied for: {file.name}. Skipping.")
            fail_count += 1

        except Exception as e:
            logger.warning(f"Failed to move {file.name}: {e}. Skipping.")
            fail_count += 1

    logger.info(
        f"Transfer complete — {success_count} moved, {fail_count} failed."
    )

    # Clean up empty folders left behind in local download path
    _cleanup_empty_folders(source)

    return True


def _cleanup_empty_folders(path: Path) -> None:
    """
    Removes empty subdirectories from the local download folder
    after files have been moved to the pendrive.

    Args:
        path (Path): Root folder to clean up.
    """
    for folder in sorted(path.rglob("*"), reverse=True):
        if folder.is_dir():
            try:
                folder.rmdir()  # Only removes if empty
            except OSError:
                pass  # Folder is not empty, leave it