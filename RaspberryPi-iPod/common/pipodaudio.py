import os
import music_tag 
#import pandas as pd
#import pygame
#from datetime import datetime
import pygame
from pygame import mixer
from common.pipodconfiguration import piPodConfiguration
from common.musicdatabase import MusicDB


class AudioPlayback():
    def __init__(self):
        pygame.init()
        self.MUSIC_END = pygame.USEREVENT + 100
#        print('self.MUSICENDEVENT:', self.MUSICENDEVENT)
        self.musicDB = MusicDB()
        self.config = piPodConfiguration()
        self.musicRootDirectory = self.config.MusicRootDirectory
        self.CurrentDuration = 0
        self.MusicStarted = False
        mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
        mixer.init()
        mixer.music.set_endevent(self.MUSIC_END)
        
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
    
    def getNextTrack(self):
        dfNextTrack = self.musicDB.musicDB.getNowPlayingNextTrack()
        return dfNextTrack
    
    def setTrack(self,  TrackId,  StartPosition = 0):
        sTrackId = TrackId
        dfTrack = self.musicDB.getTrackFromDB(sTrackId)
        self.CurrentTrackFile = self.TrackFile = os.path.join(dfTrack['FileLocation'].iloc[0],  dfTrack['FileName'].iloc[0])
#        self.CurrentTrackID3 = self.getTrackID3Tags(self.CurrentTrackFile)
        pygame.mixer.music.load(self.CurrentTrackFile)
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(StartPosition)
        pygame.mixer.music.pause()
#        return self.CurrentTrackID3
        
#    def  setNextTrack(self, NextTrackFile):
#        self.sNextTrackFile
    
    def playTrack(self):
        mixer.music.unpause()
#        if self.MusicStarted == False:
#            self.MusicStarted = True
#            mixer.music.play()
#        else:
#            mixer.music.unpause()
    
    def pauseTrack(self):
        mixer.music.pause()
        
    def rewindTrack(self):
        mixer.music.play(start=0.0)
    
    def stopTrack(self):
        pass
        
    def nextTrack(self):
        pass
        
    def getCurrentPosition(self):
        currentPosition = mixer.music.get_pos()/1000
        return currentPosition
     
    def getCurrentDuration(self):
        return self.CurrentDuration
