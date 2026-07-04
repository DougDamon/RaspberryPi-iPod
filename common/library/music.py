# common/library/music.py
import pandas as pd

from common.library.music_database import MusicDB


class MusicLibraryService:
    def __init__(self):
        self.db = MusicDB()

    def get_track(self, track_id):
        df_track = self.db.getTrackFromDB(track_id)

        if df_track is None or df_track.empty:
            return None

        return df_track

    def get_current_track(self):
        df_track = self.db.getCurrentTrack()

        if df_track is None or df_track.empty:
            return None

        if "TrackId" not in df_track.columns:
            return None

        return df_track

    def get_downloaded_playlists(self):
        df_playlists = self.db.getDownloadedPlaylists()

        if df_playlists is None or df_playlists.empty:
            return pd.DataFrame()

        return df_playlists

    def get_playlist_tracks(self, playlist_id):
        df_tracks = self.db.getPlaylistTracksFromDB(playlist_id)

        if df_tracks is None or df_tracks.empty:
            return pd.DataFrame()

        return df_tracks
