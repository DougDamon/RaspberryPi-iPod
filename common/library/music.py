# common/library/music.py

from common.library.music_database import MusicDB


class MusicLibraryService:
    """
    Music-specific library service.

    Wraps the existing MusicDB implementation and gives the rest of the app
    a clearer music-library boundary.
    """

    def __init__(self):
        self.db = MusicDB()

    def get_downloaded_playlists(self):
        return self.db.getDownloadedPlaylists()

    def get_playlist_tracks(self, playlist_id):
        return self.db.getPlaylistTracksFromDB(playlist_id)

    def get_current_playlist_id(self):
        return self.db.getCurrentPlaylistId()

    def get_current_track_id(self):
        return self.db.getCurrentTrackId()

    def get_current_track(self):
        return self.db.getCurrentTrack()
