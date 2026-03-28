from check_pendrive import check_drives
from app import download_from_channels
import time
import shutil
from pathlib import Path

# Folder where videos are downloaded on laptop

LOCAL_DOWNLOAD_PATH = Path.home() / "Videos" / "Downloaded"

# Ensure local download folder exists

LOCAL_DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)

print("Detecting existing drives...")
known_drives = check_drives()

print("Monitoring for pendrive insertion...")

while True:
    current_drives = check_drives()

    
    # Detect new drives
    new_drives = [d for d in current_drives if d not in known_drives]

    if new_drives:
        pendrive = new_drives[0]
        print(f"Pendrive connected: {pendrive}")

        # Step 1 — Download videos to laptop
        print("Downloading latest videos...")
        download_from_channels()

        # Step 2 — Prepare pendrive folder
        pendrive_path = Path(pendrive) / "Movies"
        pendrive_path.mkdir(parents=True, exist_ok=True)

        print("Moving videos to pendrive...")

        # Step 3 — Move downloaded files
        for item in LOCAL_DOWNLOAD_PATH.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(LOCAL_DOWNLOAD_PATH)
                dest = pendrive_path / relative_path

                dest.parent.mkdir(parents=True, exist_ok=True)

                try:
                    shutil.move(str(item), str(dest))
                except Exception as e:
                    print(f"Error moving {item}: {e}")

        print("Videos successfully moved to pendrive")

        # Update known drives
        known_drives = current_drives.copy()

    time.sleep(2)
    
