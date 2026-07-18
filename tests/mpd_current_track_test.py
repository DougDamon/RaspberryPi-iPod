from common.audio.player import AudioPlayback

player = AudioPlayback()

mpd_file = player.mpd.get_current_file()

print("MPD file:", mpd_file)

track_id = player.getTrackIdFromMPDPath(mpd_file)

print("TrackId:", track_id)

if track_id is not None:
    df_track = player.musicDB.getTrackFromDB(track_id)
    print(df_track[['TrackId', 'Title', 'FileLocation', 'FileName']])
