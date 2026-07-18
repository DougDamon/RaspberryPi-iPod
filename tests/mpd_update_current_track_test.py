from common.audio.player import AudioPlayback

player = AudioPlayback()

print("Before:")
print("MPD file:", player.mpd.get_current_file())
print("Current TrackId:", getattr(player, "CurrentTrackId", None))

track_id = player.updateCurrentTrackFromMPD()

print("After:")
print("Returned TrackId:", track_id)
print("Current TrackId:", getattr(player, "CurrentTrackId", None))
print("Current DB Track:")
print(player.musicDB.getCurrentTrack())
