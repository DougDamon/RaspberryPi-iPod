from common.audio.mpd_player import MPDAudioPlayback

player = MPDAudioPlayback()

print("Status:", player.status())
print("Volume:", player.get_volume())

player.volume_down()
print("Volume after down:", player.get_volume())

player.play()

print("Playing:", player.is_playing())
print("Song:", player.current_song())
print("Elapsed:", player.get_elapsed())
print("Duration:", player.get_duration())
