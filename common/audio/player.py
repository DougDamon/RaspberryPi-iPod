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
        
    def setTrackToPlay(self,  Track):
        self.Track = Track
        self.TrackFile = os.path.join(Track['FileLocation'].iloc[0],  Track['FileName'].iloc[0])
        
    def setCurrentDuration(self,  Length):
        self.CurrentDuration = round(float(str(Length)))
    
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
    
        # MPD paths are normally relative to music_directory.
        # Your database appears to store full file locations, so strip the configured
        # music root when possible.
        mpd_track_path = self.CurrentTrackFile
    
        if mpd_track_path.startswith(self.musicRootDirectory):
            mpd_track_path = os.path.relpath(mpd_track_path, self.musicRootDirectory)
    
        self.mpd.connect()
        self.mpd.client.clear()
#        print("CurrentTrackFile:", self.CurrentTrackFile)
#        print("musicRootDirectory:", self.musicRootDirectory)
#        print("mpd_track_path:", mpd_track_path)
        self.mpd.client.add(mpd_track_path)
        self.mpd.client.play()
    
#        if StartPosition > 0:
#            self.mpd.seek_current(StartPosition)
    
        # Match old pygame behavior: setTrack loads/prepares the track but leaves it paused.
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
        pass
        
    def nextTrack(self):
        pass
           
    def getCurrentDuration(self):
        return self.CurrentDuration
