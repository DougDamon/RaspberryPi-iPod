# common/library/music.py
import os

import music_tag
import pandas as pd

from common.library.music_database import MusicDB
from common.audio.mpd_player import MPDAudioPlayback


class MusicLibraryService:
    def __init__(self):
        self.db = MusicDB()
        self.mpd = MPDAudioPlayback()
        self.import_music_directory = "/home/pi/audio_import/music"
        self.music_directory = "/home/pi/audio/music"

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
    
    def get_artists(self):
        return self.db.getArtistsFromDB()
        
    def get_albums(self):
        return self.db.getAlbumsFromDB()
    
    
    def get_genres(self):
        return self.db.getGenresFromDB()
    
    
    def get_tracks_by_artist(self, artist):
        return self.db.getTracksByArtistFromDB(artist)
    
    
    def get_tracks_by_album(self, album):
        return self.db.getTracksByAlbumFromDB(album)
    
    
    def get_tracks_by_genre(self, genre):
        return self.db.getTracksByGenreFromDB(genre)
        
    def dry_run_music_import(self):
        supported_extensions = {
            ".mp3",
            ".flac",
            ".m4a",
            ".ogg",
            ".opus",
            ".wav",
        }
    
        artwork_names = {
            "cover.jpg",
            "cover.jpeg",
            "cover.png",
            "folder.jpg",
            "folder.jpeg",
            "folder.png",
            ".folder.png",
            "front.jpg",
            "front.jpeg",
            "front.png",
        }
    
        if not os.path.isdir(self.import_music_directory):
            print(
                "Import directory does not exist:",
                self.import_music_directory
            )
            return
    
        for root, directories, files in os.walk(
            self.import_music_directory
        ):
            audio_files = []
    
            for file_name in files:
                extension = os.path.splitext(file_name)[1].lower()
    
                if extension in supported_extensions:
                    audio_files.append(file_name)
    
            for file_name in sorted(audio_files):
                source_file = os.path.join(
                    root,
                    file_name
                )
    
                try:
                    tags = music_tag.load_file(source_file)
    
                    artist = str(tags["artist"]).strip()
                    album = str(tags["album"]).strip()
                    title = str(tags["title"]).strip()
                    track_number = str(tags["tracknumber"]).strip()
                    genre = str(tags["genre"]).strip()
    
                    try:
                        duration = round(
                            float(str(tags["#length"]))
                        )
                    except (ValueError, TypeError):
                        duration = 0
    
                    if not artist:
                        artist = "Unknown Artist"
    
                    if not album:
                        album = "Unknown Album"
    
                    if not title:
                        title = os.path.splitext(
                            file_name
                        )[0]
    
                    artwork_file = None
    
                    for candidate in files:
                        if candidate.lower() in artwork_names:
                            artwork_file = os.path.join(
                                root,
                                candidate
                            )
                            break
    
                    destination_directory = os.path.join(
                        self.music_directory,
                        artist,
                        album
                    )
    
                    destination_file = os.path.join(
                        destination_directory,
                        file_name
                    )
    
                    print()
                    print("=" * 60)
                    print("SOURCE")
                    print(source_file)
    
                    print()
                    print("TAGS")
                    print("Artist:", artist)
                    print("Album:", album)
                    print("Title:", title)
                    print("Track:", track_number)
                    print("Genre:", genre)
                    print("Duration:", duration)
    
                    print()
                    print("ARTWORK")
    
                    if artwork_file is None:
                        print("None")
                    else:
                        print(artwork_file)
    
                    print()
                    print("DESTINATION")
                    print(destination_file)
    
                    print()
                    print("DIRECTORY STATUS")
                    print(
                        "Artist directory exists:",
                        os.path.isdir(
                            os.path.join(
                                self.music_directory,
                                artist
                            )
                        )
                    )
                    print(
                        "Album directory exists:",
                        os.path.isdir(
                            destination_directory
                        )
                    )
    
                except Exception as error:
                    print()
                    print("=" * 60)
                    print("ERROR")
                    print(source_file)
                    print(error)

    def import_music(self):
        supported_extensions = {
            ".mp3",
            ".flac",
            ".m4a",
            ".ogg",
            ".opus",
            ".wav",
        }
    
        if not os.path.isdir(self.import_music_directory):
            print(
                "Import directory does not exist:",
                self.import_music_directory
            )
            return
            
        imported_count = 0
        
        for root, directories, files in os.walk(
            self.import_music_directory
        ):
            for file_name in sorted(files):
                extension = os.path.splitext(file_name)[1].lower()
    
                if extension not in supported_extensions:
                    continue
    
                source_file = os.path.join(
                    root,
                    file_name
                )
    
                try:
                    tags = music_tag.load_file(source_file)
    
                    artist = str(tags["artist"]).strip()
                    album = str(tags["album"]).strip()
                    title = str(tags["title"]).strip()
                    track_number = str(tags["tracknumber"]).strip()
                    genre = str(tags["genre"]).strip()
    
                    try:
                        duration = round(
                            float(str(tags["#length"]))
                        )
                    except (ValueError, TypeError):
                        duration = 0
    
                    if not artist:
                        artist = "Unknown Artist"
    
                    if not album:
                        album = "Unknown Album"
    
                    if not title:
                        title = os.path.splitext(
                            file_name
                        )[0]
    
                    destination_directory = os.path.join(
                        self.music_directory,
                        artist,
                        album
                    )
    
                    destination_file = os.path.join(
                        destination_directory,
                        file_name
                    )
    
                    if os.path.exists(destination_file):
                        print()
                        print("SKIPPED - destination already exists")
                        print(source_file)
                        print(destination_file)
                        continue
    
                    os.makedirs(
                        destination_directory,
                        exist_ok=True
                    )
    
                    os.rename(
                        source_file,
                        destination_file
                    )
    
                    track_id = self.db.addImportedTrackToDB(
                        title=title,
                        artist=artist,
                        album=album,
                        track_number=track_number,
                        genre=genre,
                        duration_seconds=duration,
                        file_location=destination_directory,
                        file_name=file_name
                    )
                    imported_count += 1
                    print()
                    print("IMPORTED")
                    print("TrackId:", track_id)
                    print("Source:", source_file)
                    print("Destination:", destination_file)
    
                except Exception as error:
                    print()
                    print("IMPORT ERROR")
                    print(source_file)
                    print(error)
        if imported_count > 0:
            print()
            print("Updating MPD library...")
            self.mpd.update_library()
            print("MPD library update started.")                
