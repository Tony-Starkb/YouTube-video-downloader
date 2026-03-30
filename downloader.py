"""
downloader.py — Handles downloading videos from YouTube channels
Uses yt-dlp with archive tracking to ensure videos are never
downloaded twice, even across multiple pendrive insertions.
"""

import yt_dlp
from pathlib import Path
from typing import List
from config import LOCAL_DOWNLOAD_PATH, ARCHIVE_FILE, VIDEO_FORMAT, CHANNELS
from logger import logger


def _build_ydl_options() -> dict:
    """
    Builds and returns the yt-dlp configuration dictionary.
    Kept separate so options can be easily modified or extended.
    """
    return {
        # Video quality setting from config
        "format": VIDEO_FORMAT,

        # Save videos organized by uploader name
        "outtmpl": str(LOCAL_DOWNLOAD_PATH / "%(uploader)s" / "%(title)s.%(ext)s"),

        # Archive file prevents re-downloading already downloaded videos
        "download_archive": str(ARCHIVE_FILE),

        # Skip unavailable videos without stopping the entire process
        "ignoreerrors": True,

        # Suppress yt-dlp's own verbose output — we handle logging ourselves
        "quiet": True,
        "no_warnings": True,

        # Show download progress
        "progress_hooks": [_progress_hook],
    }


def _progress_hook(status_info: dict) -> None:
    """
    Callback function triggered by yt-dlp during download.
    Logs download completion events.
    """
    if status_info.get("status") == "finished":
        filename = Path(status_info["filename"]).name
        logger.info(f"Downloaded: {filename}")


def download_from_channels(channels: List[str] = None) -> bool:
    """
    Downloads latest videos from all configured YouTube channels.
    Skips videos already present in the download archive.

    Args:
        channels (List[str], optional): List of channel URLs to download from.
                                        Defaults to CHANNELS from config.

    Returns:
        bool: True if download process completed, False if an error occurred.
    """
    channels = channels or CHANNELS

    # Ensure the local download directory exists
    LOCAL_DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
    ARCHIVE_FILE.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting download from {len(channels)} channel(s)...")

    try:
        ydl_opts = _build_ydl_options()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(channels)

        logger.info("All channel downloads completed successfully.")
        return True

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download error occurred: {e}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error during download: {e}")
        return False