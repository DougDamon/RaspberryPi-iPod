# piPod - Raspberry Pi iPod Clone

A Python-based music player for Raspberry Pi with YouTube download capabilities and a Qt-based GUI.

## Features

- Music playback with playlist management
- YouTube playlist download and conversion
- Qt-based touchscreen GUI
- Album art display
- SQLite music database
- Theme support

## Requirements

- Python 3.7+
- Raspberry Pi (tested on Pi 3/4)
- Qt5/PySide6 for GUI
- yt-dlp for YouTube downloads
- pygame or vlc for audio playback

## Installation

```bash
# Clone repository
git clone https://github.com/DougDamon/RaspberryPi-iPod.git
cd RaspberryPi-iPod

# Install dependencies
pip install -r requirements.txt

# Configure
cp piPod.cfg.example piPod.cfg
# Edit piPod.cfg with your settings
