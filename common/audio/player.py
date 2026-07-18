import os
import music_tag

import pygame

from common.config.settings import ConfigService
from common.library.music_database import MusicDB
from common.audio.mpd_player import MPDAudioPlayback

class AudioPlayback():
    def __init__(self):
        pygame.init()

        # Keep this event defined for now so the rest of the app does not break.
        # MPD will not use pygame's endevent, so end-of-track handling will need
        # a later replacement.
        self.MUSIC_END = pygame.USEREVENT + 100

        self.musicDB = MusicDB()
        self.config = ConfigService()
        self.musicRootDirectory = self.config.MusicRootDirectory

        self.mpd = MPDAudioPlayback()

        self.CurrentDuration = 0
        self.AudioPlaying = False
        self.Repeat = 'Off'
        self.Shuffle = 'Off'
        self.CurrentTrackFile = None
    def getAudioPlayingStatus(self):
        self.AudioPlaying = self.mpd.is_playing()
        return self.AudioPlaying
    
    def setAudioPlayingStatus(self, Status):
        self.AudioPlaying = Status
    
    def setPlaylist(self, PlaylistId, SelectedTrackId=None):
        dfPlaylistTracks = self.musicDB.getPlaylistTracksFromDB(PlaylistId)
    
        mpd_paths = []
        selected_position = 0
    
        for index, row in dfPlaylistTracks.reset_index(drop=True).iterrows():
            track_id = row['TrackId']
    
            dfTrack = self.musicDB.getTrackFromDB(track_id)
    
            mpd_path = self.getMPDTrackPath(
                dfTrack['FileLocation'].iloc[0],
                dfTrack['FileName'].iloc[0]
            )
    
            mpd_paths.append(mpd_path)
    
            if SelectedTrackId is not None and track_id == SelectedTrackId:
                selected_position = index
    
        self.mpd.add_tracks(mpd_paths)
        self.mpd.play_position(selected_position)
        self.mpd.pause()
        self.setAudioPlayingStatus(False)
    
        return selected_position
    
    def setTrackToPlay(self,  Track):
        self.Track = Track
        self.TrackFile = os.path.join(Track['FileLocation'].iloc[0],  Track['FileName'].iloc[0])
        
    def setCurrentDuration(self,  Length):
        self.CurrentDuration = round(float(str(Length)))

    def getMPDTrackPath(self, file_location, file_name):
        full_path = os.path.join(file_location, file_name)
    
        if full_path.startswith(self.musicRootDirectory):
            return os.path.relpath(full_path, self.musicRootDirectory)
    
        return full_path
        
    def getTrackIdFromMPDPath(self, mpd_path):
        if mpd_path is None or mpd_path == '':
            return None
    
        # MPD gives us a path relative to musicRootDirectory.
        full_path = os.path.join(self.musicRootDirectory, mpd_path)
    
        file_location = os.path.dirname(full_path)
        file_name = os.path.basename(full_path)
    
        # Normalize trailing slash differences because your DB may store
        # FileLocation with or without a trailing slash.
        file_location_no_slash = file_location.rstrip('/')
        file_location_with_slash = file_location_no_slash + '/'
    
        df_matches = self.musicDB.getTrackTableFromDB()
    
        df_matches = df_matches[
            (
                (df_matches['FileLocation'] == file_location_no_slash) |
                (df_matches['FileLocation'] == file_location_with_slash)
            ) &
            (df_matches['FileName'] == file_name)
        ]
    
        if df_matches.empty:
            print("No database match for MPD path:", mpd_path)
            print("Expected FileLocation:", file_location_no_slash)
            print("Expected FileName:", file_name)
            return None
    
        return df_matches['TrackId'].iloc[0]

    def updateCurrentTrackFromMPD(self):
        mpd_path = self.mpd.get_current_file()
    
        if mpd_path is None or mpd_path == '':
            return None
    
        track_id = self.getTrackIdFromMPDPath(mpd_path)
    
        if track_id is None:
            return None
    
        dfTrack = self.musicDB.getTrackFromDB(track_id)
    
        if dfTrack.empty:
            return None
    
        duration = int(dfTrack['DurationSeconds'].iloc[0])
        current_position = int(round(self.getCurrentPosition()))
    
        self.CurrentTrackId = track_id
        self.CurrentDuration = duration
    
        self.musicDB.setCurrentTrack(
            track_id,
            duration,
            0,
            current_position
        )
    
        return track_id
    
    def getTrackID3Tags(self, TrackId):
        sTrackId = TrackId
        dfTrack = self.musicDB.getTrackFromDB(sTrackId)
        sTrackFile  = os.path.join(dfTrack['FileLocation'].iloc[0],  dfTrack['FileName'].iloc[0])
        self.CurrentTrackID3 = music_tag.load_file(sTrackFile)
        self.setCurrentDuration(self.CurrentTrackID3['#length'])
        return self.CurrentTrackID3 
    
#    def getNextTrack(self):
#        dfNextTrack = self.musicDB.getNowPlayingNextTrack()
#        return dfNextTrack
    
    def setTrack(self, TrackId, StartPosition=0):
        sTrackId = TrackId
        dfTrack = self.musicDB.getTrackFromDB(sTrackId)
    
        self.CurrentTrackFile = self.TrackFile = os.path.join(
            dfTrack['FileLocation'].iloc[0],
            dfTrack['FileName'].iloc[0]
        )
    
        mpd_track_path = self.getMPDTrackPath(
            dfTrack['FileLocation'].iloc[0],
            dfTrack['FileName'].iloc[0]
        )
    
        self.mpd.clear_playlist()
        self.mpd.add_track(mpd_track_path)
        self.mpd.play_position(0)
    
        # Resume seeking stays disabled for now.
        # if StartPosition > 0:
        #     self.mpd.seek_current(StartPosition)
    
        self.mpd.pause()
        self.setAudioPlayingStatus(False)

    def playTrack(self):
        self.mpd.resume()
        self.setAudioPlayingStatus(True)
    
    def pauseTrack(self):
        self.mpd.pause()
        self.setAudioPlayingStatus(False)
        
    def rewindTrack(self):
        self.mpd.seek_current(0)
        self.setAudioPlayingStatus(True)
    
    def getCurrentPosition(self):
        return self.mpd.get_elapsed()
    
    def stopTrack(self):
        self.mpd.stop()
        self.setAudioPlayingStatus(False)
        
    def nextTrack(self):
        self.mpd.next()
        self.setAudioPlayingStatus(True)
    
    def previousTrack(self):
        self.mpd.previous()
        self.setAudioPlayingStatus(True)
        
    def setRepeatOff(self):
        self.mpd.repeat_off()
        self.Repeat = 'Off'
    
    def setRepeatPlaylist(self):
        self.mpd.repeat_playlist()
        self.Repeat = 'On'
    
    def setRepeatOne(self):
        self.mpd.repeat_one()
        self.Repeat = 'One'
    
    def setShuffleOff(self):
        self.mpd.shuffle_off()
        self.Shuffle = 'Off'
    
    def setShuffleOn(self):
        self.mpd.shuffle_on()
        self.Shuffle = 'On'

    def getCurrentDuration(self):
        return self.CurrentDuration
