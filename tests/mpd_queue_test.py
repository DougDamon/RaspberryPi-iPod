# tests/mpd_queue_test.py

from common.audio.player import AudioPlayback

player = AudioPlayback()

# Replace these with known IDs from your database.
playlist_id = 'PLtoBJCi7zQr9FBKCK-QXMcOlQj5IwHvPF'
track_id = 'HdIZzlD7nmo'

df_tracks = player.musicDB.getPlaylistTracksFromDB(playlist_id)

position = player.setPlaylist(playlist_id, track_id)

print("Loaded playlist position:", position)
print("MPD status:", player.mpd.status())
print("Current song:", player.mpd.current_song())

player.playTrack()
print("After play:", player.mpd.status())
