#import os
import music_tag 
#import pandas as pd
#import pygame
#from datetime import datetime
from pygame import mixer
from common.pipodconfiguration import piPodConfiguration
from common.musicdatabase import MusicDB


class AudioPlayback():
    def __init__(self):
        self.musicDB = MusicDB()
        self.config = piPodConfiguration()
        self.musicRootDirectory = self.config.MusicRootDirectory
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
        pygame.mixer.init()
    def setTrack(self,  TrackFile):
        self.trackFile = TrackFile
        self.audio = MP3(self.trackFile)
    def  setNextTrack(self, NextTrackFile):
        self.sNextTrackFile
    
    def playTrack(self):
        
    
    def pauseTrack(self):
        
    
    def stopTrack(self):
        
    def nextTrack(self):
        

