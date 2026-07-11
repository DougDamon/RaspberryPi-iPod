import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from common.audio.mpd_player import MPDAudioPlayback

player = MPDAudioPlayback()

print("Status:", player.status())
print("Song:", player.current_song())

print("Volume:", player.get_volume())
player.volume_down()
print("Volume after down:", player.get_volume())

player.play()
print("Playing:", player.is_playing())
print("Elapsed:", player.get_elapsed())
print("Duration:", player.get_duration())
