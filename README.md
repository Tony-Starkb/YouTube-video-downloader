# YouTube Auto-Downloader

A background automation system that detects when a pendrive is plugged in and automatically downloads the latest videos from configured YouTube channels — no human input required after setup.

---

## How It Works

1. System starts and records all currently connected drives
2. Monitors continuously for any new drive being plugged in
3. On pendrive detection → downloads latest videos from configured channels
4. Moves downloaded videos to the pendrive (organized by channel)
5. Returns to monitoring state and waits for next insertion

Videos already downloaded are tracked via an archive file — they are **never re-downloaded**, even across multiple pendrive insertions.

---

## Project Structure

```
youtube_downloader/
│
├── main.py            # Entry point — runs the monitoring loop
├── config.py          # All settings (channels, paths, quality) — edit this file
├── drive_monitor.py   # Detects newly connected drives
├── downloader.py      # Handles YouTube video downloading via yt-dlp
├── transfer.py        # Moves downloaded videos to the pendrive
├── logger.py          # Centralized logging with timestamps
└── requirements.txt   # Project dependencies
```

---

## Setup & Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your channels

Open `config.py` and add your YouTube channel URLs:

```python
CHANNELS = [
    "https://www.youtube.com/@YourChannel/videos",
    "https://www.youtube.com/@AnotherChannel/videos",
]
```

### 3. Run the system

```bash
python main.py
```

The system will start monitoring. Plug in a pendrive and it handles everything automatically.

---

## Configuration Options (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `LOCAL_DOWNLOAD_PATH` | `~/Videos/Downloaded` | Temporary folder on laptop |
| `PENDRIVE_FOLDER_NAME` | `Movies` | Folder created on pendrive |
| `VIDEO_FORMAT` | `best` | Video quality (`best`, `worst`) |
| `POLL_INTERVAL_SECONDS` | `3` | How often to check for new drives |
| `EXCLUDED_DRIVES` | `{"C:\\"}` | Drives to always ignore |

---

## Tech Stack

- **Python 3.8+**
- **yt-dlp** — YouTube video downloading with archive tracking
- **os / pathlib** — Drive detection and file system operations
- **shutil** — Safe file transfer with error handling

---

## Requirements

```
yt-dlp
```

> **Note:** This system is designed for Windows. Drive detection uses Windows-style drive letters (C:\\, D:\\, etc.).
