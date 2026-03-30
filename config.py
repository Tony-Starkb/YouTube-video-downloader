"""
config.py — Central configuration for YouTube Auto-Downloader
All user settings are managed here. No need to touch other files.
"""

from pathlib import Path

# ─────────────────────────────────────────────
# DOWNLOAD SETTINGS
# ─────────────────────────────────────────────

# Folder on your laptop where videos are temporarily stored before moving to pendrive
LOCAL_DOWNLOAD_PATH = Path.home() / "Videos" / "Downloaded"

# Archive file — tracks already downloaded videos so they are never re-downloaded
ARCHIVE_FILE = LOCAL_DOWNLOAD_PATH / "downloaded_archive.txt"

# Folder name that will be created on the pendrive
PENDRIVE_FOLDER_NAME = "Movies"

# ─────────────────────────────────────────────
# YOUTUBE CHANNELS TO MONITOR
# ─────────────────────────────────────────────
# Add or remove channel URLs here.
# Format: "https://www.youtube.com/@ChannelName/videos"

CHANNELS = [
    "https://www.youtube.com/@rkumarv/videos",
    "https://www.youtube.com/@EnesYilmazer/videos",
    "https://www.youtube.com/@Gavren/videos",
]

# ─────────────────────────────────────────────
# VIDEO QUALITY SETTINGS
# ─────────────────────────────────────────────
# "best"         → Best available quality
# "bestvideo"    → Best video only (no audio)
# "worst"        → Smallest file size

VIDEO_FORMAT = "best"

# ─────────────────────────────────────────────
# SYSTEM SETTINGS
# ─────────────────────────────────────────────

# How often (in seconds) the system checks for a new pendrive
POLL_INTERVAL_SECONDS = 3

# Drive letters to always ignore (system drives)
EXCLUDED_DRIVES = {"C:\\"}