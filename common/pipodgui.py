import os
# import time
import datetime

import pygame
import pygame_gui

#from pygame.font import Font
from pygame_gui.core import ObjectID
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_selection_list import UISelectionList
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_image import UIImage
from pygame_gui.elements.ui_progress_bar import UIProgressBar

from io import BytesIO

from PIL import  Image
from common.pipodconfiguration import piPodConfiguration
from common.pipodaudio import AudioPlayback
from common.musicdatabase import MusicDB
#from common.rotaryencoder import RotaryEncoder
   
class piPodGUI(AudioPlayback, MusicDB):
    def __init__(self):
#        super().__init__()
        AudioPlayback.__init__(self)
        MusicDB.__init__(self)
        pygame.display.set_caption('piPod')
        
        # piPod config file
        self.configuration = piPodConfiguration()
        self.Screens = self.configuration.Screens
        self.ScreenNavigation = self.configuration.ScreenNavigation
        
        #pygame_gui Theme file
        themeFile =os.path.join(self.configuration.ThemeDirectory,  self.configuration.ThemeFile)
        
        # pygame_gui setup
        self.window_surface = pygame.display.set_mode((325,245))
        self.background = pygame.Surface((325,245))
        self.background.fill(pygame.Color('aquamarine'))
        self.manager = UIManager((320,240),  themeFile)
       
#        self.piPodAudio = AudioPlayback()
#        self.musicDB = MusicDB()
        
#        Setup Windows
        self.windowMainScreen = UIWindow(pygame.Rect((1, 1), (320,240))
                                                                 ,manager=self.manager
                                                                 ,element_id='window') 
        
        self.windowNowPlaying = UIWindow(pygame.Rect((1, 1), (320,240))
                                                                 ,manager=self.manager
                                                                 ,element_id='window') 
 
        self.windowMusic = UIWindow(pygame.Rect((1, 1), (320,240))
                                                                 ,manager=self.manager
                                                                 ,element_id='window')  

        self.windowAvailablePlaylists = UIWindow(pygame.Rect((1, 1), (320,240))
                                                                 ,manager=self.manager
                                                                 ,element_id='window') 
                                                                
        self.windowPlaylistTracks = UIWindow(pygame.Rect((1, 1), (320,240))
                                                                 ,manager=self.manager
                                                                 ,element_id='window') 
        
        self.CurrentPlaylistId = self.getCurrentPlaylistId()
        self.CurrentPlaylistInfo = self.getCurrentPlaylistInfo()
            
        self.CurrentTrackId = self.getCurrentTrackId()
#        print(self.CurrentPlaylistId,  self.CurrentTrackId)
        self.NextPlaylistId = None
        self.NextTrackId = None
        self.AutoPlayOnStart = False
        

        self.NoAblumArtFile = os.path.join(self.configuration.ImageDirectory,  self.configuration.NoAlbumArt)
#        print(self.NoAblumArtFile)
        self.ImageNoAblumArt = pygame.image.load(self.NoAblumArtFile)
        self.CurrentAlbumArt = self.ImageNoAblumArt
        self.CurrentTitle = ''
        self.CurrentArtist = ''
        self.CurrentAlbum = ''
        self.CurrentGenre = ''
        self.CurrentPlaylist = ''
        self.CurrentPosition = 0
        self.CurrentPositionPercent = 0
        self.StartPlaybackPosition = 0
        self.CurrentPositionFormat = '00:00'
        self.CurrentDurationSeconds = 0
        self.CurrentDurationFormat = '00:00'
        
        # Set True when Screen is Initialized
        self.MusicScreenInit = False
        self.AvailablePlaylistsScreenInit = False
        
        self.MainScreen()
        self.MusicScreen()
        self.AvailablePlaylistsScreen()
        self.PlaylistTracksScreen()
        self.NowPlayingScreen()
        
        self.windowMusic.hide()
        self.windowAvailablePlaylists.hide()
        self.windowPlaylistTracks.hide()
        self.windowNowPlaying.hide()
        self.MainScreenShow()
        
        self.navigationPath = []
        self.QUIT = pygame.QUIT
        self.UI_BUTTON_PRESSED = pygame_gui.UI_BUTTON_PRESSED
        self.UI_SELECTION_LIST_NEW_SELECTION = pygame_gui.UI_SELECTION_LIST_NEW_SELECTION
    
    def getClock(self):
        return pygame.time.Clock()
      
    def getEvent(self):
        events = pygame.event.get()
        return events
        
    def updateDisplay(self):
        pygame.display.update()
        
    def quit(self):
        pygame.quit()
    
    def drawScreen(self):
        self.manager.draw_ui(self.window_surface)
        
    def formatTrackTime(self,  Seconds):
        if Seconds < 3600:
            return str(datetime.timedelta(seconds=Seconds))[-5:]
        else:
            return str(datetime.timedelta(seconds=self.Seconds))
    def getNavigationPath(self):  
        return self.navigationPath
    
    def  popNavigationPath(self):
        return self.navigationPath.pop()
    
    def pushNavigationPath(self,  ScreenName):
        self.navigationPath.append(ScreenName)
    
    def MainScreen(self):
        self.bNowPlaying = UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                                       text='Now Playing',
                                                       container = self.windowMainScreen ,#self.containerMainWindow,
                                                       manager = self.manager, 
                                                       object_id=ObjectID(class_id='@navigation_buttons'))
    
        self.bMusic = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                             text='Music',
                                             container = self.windowMainScreen, #self.containerMainWindow,
                                             manager=self.manager, 
                                             object_id=ObjectID(class_id='@navigation_buttons'))

        self.bOTR = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                           text='OTR',
                                           container = self.windowMainScreen , #self.containerMainWindow,
                                           manager=self.manager, 
                                           object_id=ObjectID(class_id='@navigation_buttons'))

        self.bAudiobooks = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                                      text='Audiobooks',
                                                      container = self.windowMainScreen , #self.containerMainWindow,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@navigation_buttons'))

        self.bGames = UIButton(relative_rect=pygame.Rect((12, 120), (300, 24)),
                                               text='Games',
                                               container = self.windowMainScreen , #self.containerMainWindow,
                                               manager=self.manager, 
                                               object_id=ObjectID(class_id='@navigation_buttons'))

        self.bManagement = UIButton(relative_rect=pygame.Rect((12, 150), (300, 24)),
                                                         text='Mangement',
                                                         container = self.windowMainScreen , #self.containerMainWindow,
                                                         manager=self.manager, 
                                                         object_id=ObjectID(class_id='@navigation_buttons'))

        self.window_surface.blit(self.background, (0, 0))
    
    def MainScreenHide(self):
        self.windowMainScreen.hide() #self.containerMainWindow.hide()
        self.window_surface.blit(self.background, (0, 0))

    def MainScreenShow(self):
        if self.CurrentPlaylistId == None or self.CurrentTrackId == None:
            self.bNowPlaying.disable()
        self.windowMainScreen.show() 
        pygame.display.flip()
#    def NavigateMainScreen(self):
        
    def NowPlayingScreen(self): #, SelectedPlaylistId,  SelectedTrackId):
        self.lblTrackTitle = UILabel(relative_rect=pygame.Rect((177,5 ), (120, 21)),
                                                   text = self.CurrentTitle,
                                                   container = self.windowNowPlaying,
                                                   manager=self.manager, 
                                                   object_id=ObjectID(class_id='@now_playing_labels'))
        self.lblTrackArtist = UILabel(relative_rect=pygame.Rect((177,25 ), (120, 21)),
                                                     text = self.CurrentArtist, 
                                                     container = self.windowNowPlaying,
                                                     manager=self.manager, 
                                                     object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.lblTrackAlbum = UILabel(relative_rect=pygame.Rect((177,45 ), (120, 21)),
                                                       text = self.CurrentAlbum,
                                                       container = self.windowNowPlaying,
                                                       manager=self.manager, 
                                                       object_id=ObjectID(class_id='@now_playing_labels'))
                        
        self.lblTrackGenre = UILabel(relative_rect=pygame.Rect((177,65 ), (120, 21)),
                                                      text = self.CurrentGenre,
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.lblTrackPlaylist = UILabel(relative_rect=pygame.Rect((177, 85), (120, 21)),
                                                        text = self.CurrentPlaylist , 
                                                        container = self.windowNowPlaying,
                                                        manager=self.manager, 
                                                        object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.imgAlbumArt = UIImage(relative_rect=pygame.Rect((10, 0 ), (128, 128)),
                                                       image_surface=self.CurrentAlbumArt, 
                                                       container = self.windowNowPlaying,
                                                       manager=self.manager)
                                                       
        self.bPlay = UIButton(relative_rect=pygame.Rect((210, 120 ), (50, 50)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#play_button'))
                                                                                      
        self.bPause = UIButton(relative_rect=pygame.Rect((210, 120 ), (50, 50)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#pause_button'))   
        
        self.bForward = UIButton(relative_rect=pygame.Rect((260, 120 ), (50, 50)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#forward_button'))   

        self.bRewind = UIButton(relative_rect=pygame.Rect((160, 120 ), (50, 50)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#rewind_button'))   
                                                                                      
        self.bRepeatOff = UIButton(relative_rect=pygame.Rect((110,  130), (25, 25)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#repeat_off_button')) 
        
        self.bRepeatOn = UIButton(relative_rect=pygame.Rect((110,  130), (25, 25)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#repeat_on_button')) 
                                                                                      
        self.bRepeatOne = UIButton(relative_rect=pygame.Rect((110,  130), (25, 25)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#repeat_one_button'))
        
        self.bShuffleOff = UIButton(relative_rect=pygame.Rect((10,  130), (25, 25)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#shuffle_off_button'))
                                                                                      
        self.bShuffleOn = UIButton(relative_rect=pygame.Rect((10,  130), (25, 25)),
                                                      text='',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#shuffle_on_button'))
                                                                                      
        self.bBack = UIButton(relative_rect=pygame.Rect((10, 210), (50, 25)),
                                                      text='Back',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@small_navigation_buttons', 
                                                                                      object_id='#back_button'))   

        self.bHome = UIButton(relative_rect=pygame.Rect((65, 210), (50, 25)),
                                                      text='Home',
                                                      container = self.windowNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@small_navigation_buttons', 
                                                                                      object_id='#home_button')) 
                                                                                      
        
                                                                                      
        self.pbarCurrentPosition = UIProgressBar(relative_rect=pygame.Rect((58, 180), (210, 15)),
                                                                          container = self.windowNowPlaying,
                                                                          manager=self.manager, 
                                                                          object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                                          object_id='#current_position_bar'))
                                                                                                       
        self.lblCurrentPosition = UILabel(relative_rect=pygame.Rect((2, 178), (56, 20)),
                                                            text=self.CurrentPositionFormat,
                                                            container = self.windowNowPlaying,
                                                            manager=self.manager, 
                                                            object_id=ObjectID(class_id='@now_playing_labels'))
        
        self.lblTrackDuration = UILabel(relative_rect=pygame.Rect((263, 178), (56, 20)),
                                                            text=self.CurrentDurationFormat,
                                                            container = self.windowNowPlaying,
                                                            manager=self.manager, 
                                                            object_id=ObjectID(class_id='@now_playing_labels'))
   
        self.bPause.hide()
#        self.bRepeatOn.hide()
#        self.bRepeatOne.hide()
#        self.bRepeatOff.show()
#        self.bRepeatOff.select()
#        self.bRepeatOff.unselect()
        pygame.display.flip()
       
    def NowPlayingScreenHide(self):
        self.windowNowPlaying.hide()
        
    def ShowPlayButton(self):
        self.bPlay.hide()
        self.bPause.show()
        
    def ShowPauseButton(self):
        self.bPause.hide()
        self.bPlay.show()
        
    def Play(self):
        if self.CurrentTrackId != None:
            self.ShowPlayButton()
            self.bPlay.select()
            self.playTrack()
        
    def Pause(self):
        self.pauseTrack()
        self.ShowPauseButton()
        self.bPause.select()
        
    def ShowRepeatButtonOff(self):
        self.bRepeatOn.hide()
        self.bRepeatOne.hide()
        self.bRepeatOff.show()
        
    def ShowRepeatButtonOn(self):
        self.bRepeatOff.hide()
        self.bRepeatOne.hide()
        self.bRepeatOn.show()
    
    def ShowRepeatButtonOne(self):
        self.bRepeatOff.hide()
        self.bRepeatOn.hide()
        self.bRepeatOne.show()
    
    def ShowShuffleButtonOff(self):
        self.bShuffleOn.unselect()
        self.bShuffleOn.hide()
        self.bShuffleOff.show()
        
    
    def ShowShuffleButtonOn(self):
        self.bShuffleOff.unselect()
        self.bShuffleOff.hide()
        self.bShuffleOn.show()
    
    def RepeatOff(self):
        self.Repeat = 'Off'
        self.ShowRepeatButtonOff()
        self.bRepeatOff.select()
        
    def RepeatOn(self):
        self.Repeat = 'On'
        self.ShowRepeatButtonOn()
        self.bRepeatOn.select()
        
    def RepeatOne(self):
        self.Repeat = 'One'
        self.ShowRepeatButtonOne()
        self.bRepeatOne.select()
        
    def  ShuffleOff(self):
        self.Shuffle = 'Off'
        self.unshuffleCurrentPlaylist()
        self.ShowShuffleButtonOff()
        self.bShuffleOff.select()
        
    def  ShuffleOn(self):
        self.Shuffle = 'On'
        self.shuffleCurrentPlaylist()
        self.ShowShuffleButtonOn()    
        self.bShuffleOn.select()
#    def setCurrentPlaylist(self, PlaylistId):
#        self.CurrentPlaylistId = PlaylistId
#        
#        CurrentTrackId = TrackId
#        self.setCurrentPlaylist(self.CurrentPlaylistId)
#        self.CurrentPlaylistInfo = self.getCurrentPlaylistInfo()
        
    def setSelectedTrack(self, TrackId):
        self.CurrentTrackId = TrackId
        dfTrack = self.getTrackFromDB(self.CurrentTrackId)
        CurrentDurationSeconds = dfTrack['DurationSeconds'][0].item()
        self.setCurrentTrack(self.CurrentTrackId, CurrentDurationSeconds)
        
    def NowPlayingScreenShow(self):
        dfCurrentTrack = self.getCurrentTrack()
        self.CurrentTrackId = dfCurrentTrack['TrackId'][0]
        self.StartPlaybackPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition)
        
        currentTrackID3 = self.getTrackID3Tags(self.CurrentTrackId)
        currentPlaylist = self.getPlaylistInfoFromDB(self.CurrentPlaylistId)
        currentArtwork = currentTrackID3['artwork'] 
        bytesCurrentImage = currentArtwork.first.data
        pilCurrentImage = Image.open(BytesIO(bytesCurrentImage))
        
        pilCurrentImage = pilCurrentImage.resize((150, 150), 0)
        self.CurrentAlbumArt =  pygame.image.frombytes(pilCurrentImage.tobytes('raw'), (150, 150), 'RGB')
        self.CurrentTitle = str(currentTrackID3['title'])
        self.CurrentArtist = str(currentTrackID3['artist'])
        self.CurrentAlbum = str(currentTrackID3['album'])
        self.CurrentGenre = str(currentTrackID3['genre'])
        self.CurrentPlaylist = currentPlaylist.loc[0]['Playlist']
       
        self.CurrentDurationSeconds = round(float(str(currentTrackID3['#length'])))
        self.CurrentDurationFormat = self.formatTrackTime(self.CurrentDurationSeconds)
        
        
        self.setTrack(self.CurrentTrackId,  self.StartPlaybackPosition)
        
        self.windowNowPlaying.show()
        self.imgAlbumArt.set_image(self.CurrentAlbumArt)
        self.lblTrackTitle.set_text(self.CurrentTitle )
        self.lblTrackArtist.set_text(self.CurrentArtist)
        self.lblTrackAlbum.set_text(self.CurrentAlbum)
        self.lblTrackGenre.set_text(self.CurrentGenre)
        self.lblTrackPlaylist.set_text(self.CurrentPlaylist)
        self.lblCurrentPosition.set_text(self.CurrentPositionFormat)
        self.lblTrackDuration.set_text(self.CurrentDurationFormat)
        self.ShowRepeatButtonOff()
        self.ShowShuffleButtonOff()
        pygame.display.flip()
        if self.AutoPlayOnStart:
            self.Play()
        else:
            self.Pause()
            
    def NextTrackNowPlaying(self):
        if self.Repeat == 'One':
            # Repeat Track is on.  Set the starting position to 0 and start the track
            self.StartPlaybackPosition = 0
            self.setCurrentTrack(self.CurrentTrackId,  self.CurrentDurationSeconds,  0, 0)
            self.Play()
            return
        else:
            #Normal play.  Select the next track in the Playlist
            self.setNextTrack()
        
        if self.NextTrackId == None and self.Repeat != 'On':
            # The playlist has finished and repeat has not been set
            return
        elif self.NextTrackId == None and self.Repeat == 'On':
            # The Playlist is finished and repeat playlist is on
            # Set the NextPlaylist to the current
            # Set the new current track to the first track of the selected playlist
            dfFirstTrack = self.getFirstTrack(self.CurrentPlaylistId)
            self.NextTrackId = dfFirstTrack['TrackId'][0]

        
        dfCurrentTrack = self.getTrackFromDB(self.NextTrackId)
        self.CurrentTrackId = dfCurrentTrack['TrackId'][0]
        self.StartPlaybackPosition = 0 #dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPosition = 0 #dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition)
        currentTrackID3 = self.getTrackID3Tags(self.CurrentTrackId)
        currentPlaylist = self.getPlaylistInfoFromDB(self.CurrentPlaylistId)
        currentArtwork = currentTrackID3['artwork'] 
        bytesCurrentImage = currentArtwork.first.data
        pilCurrentImage = Image.open(BytesIO(bytesCurrentImage))
        pilCurrentImage = pilCurrentImage.resize((150, 150), 0)
        self.CurrentAlbumArt =  pygame.image.frombytes(pilCurrentImage.tobytes('raw'), (150, 150), 'RGB')
        self.CurrentTitle = str(currentTrackID3['title'])
        self.CurrentArtist = str(currentTrackID3['artist'])
        self.CurrentAlbum = str(currentTrackID3['album'])
        self.CurrentGenre = str(currentTrackID3['genre'])
        self.CurrentPlaylist = currentPlaylist.loc[0]['Playlist']
        self.CurrentDurationSeconds = round(float(str(currentTrackID3['#length'])))
        self.CurrentDurationFormat = self.formatTrackTime(self.CurrentDurationSeconds)
        self.CurrentPositionPercent = (self.CurrentPosition/self.CurrentDurationSeconds) * 100
        self.setCurrentTrack(self.CurrentTrackId,  self.CurrentDurationSeconds,  0, self.StartPlaybackPosition)
        self.setTrack(self.CurrentTrackId,  self.StartPlaybackPosition)
        self.windowNowPlaying.show()
        self.imgAlbumArt.set_image(self.CurrentAlbumArt)
        self.lblTrackTitle.set_text(self.CurrentTitle )
        self.lblTrackArtist.set_text(self.CurrentArtist)
        self.lblTrackAlbum.set_text(self.CurrentAlbum)
        self.lblTrackGenre.set_text(self.CurrentGenre)
        self.lblTrackPlaylist.set_text(self.CurrentPlaylist)
        self.lblCurrentPosition.set_text(self.CurrentPositionFormat)
        self.lblTrackDuration.set_text(self.CurrentDurationFormat)
        self.pbarCurrentPosition.set_current_progress(self.CurrentPositionPercent)
        
        self.Play()
        
    def PreviousTrackNowPlaying(self):
        if self.getAdjustedCurrentPosition() >= 5:
            self.rewindTrack()
            self.resetCurrentPosition()
            return
            
        self.setPreviousTrack()
        print('PrevioiusPlaylistId:',  self.NextPlaylistId)
        print('PreviousTrackId:',  self.NextTrackId)
        if self.NextTrackId == None:
            return
            
        if self.NextPlaylistId != self.CurrentPlaylistId:
            self.setCurrentPlaylist(self.NextPlaylistId)
            self.CurrentPlaylistId = self.NextPlaylistId
        
        self.setCurrentTrack(self.NextTrackId)
        self.CurrentTrackid = self.NextTrackId
        
        dfCurrentTrack = self.getCurrentTrack()
        self.CurrentTrackId = dfCurrentTrack['TrackId'][0]
        self.StartPlaybackPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition)
        currentTrackID3 = self.getTrackID3Tags(self.CurrentTrackId)
        currentPlaylist = self.getPlaylistInfoFromDB(self.CurrentPlaylistId)
        currentArtwork = currentTrackID3['artwork'] 
        bytesCurrentImage = currentArtwork.first.data
        pilCurrentImage = Image.open(BytesIO(bytesCurrentImage))
        
        pilCurrentImage = pilCurrentImage.resize((150, 150), 0)
        self.CurrentAlbumArt =  pygame.image.frombytes(pilCurrentImage.tobytes('raw'), (150, 150), 'RGB')
        self.CurrentTitle = str(currentTrackID3['title'])
        self.CurrentArtist = str(currentTrackID3['artist'])
        self.CurrentAlbum = str(currentTrackID3['album'])
        self.CurrentGenre = str(currentTrackID3['genre'])
        self.CurrentPlaylist = currentPlaylist.loc[0]['Playlist']
       
        self.CurrentDurationSeconds = round(float(str(currentTrackID3['#length'])))
        self.CurrentDurationFormat = self.formatTrackTime(self.CurrentDurationSeconds)
        self.CurrentPositionPercent = (self.CurrentPosition/self.CurrentDurationSeconds) * 100
        self.setTrack(self.CurrentTrackId,  self.StartPlaybackPosition)
        
        self.windowNowPlaying.show()
        self.imgAlbumArt.set_image(self.CurrentAlbumArt)
        self.lblTrackTitle.set_text(self.CurrentTitle )
        self.lblTrackArtist.set_text(self.CurrentArtist)
        self.lblTrackAlbum.set_text(self.CurrentAlbum)
        self.lblTrackGenre.set_text(self.CurrentGenre)
        self.lblTrackPlaylist.set_text(self.CurrentPlaylist)
        self.lblCurrentPosition.set_text(self.CurrentPositionFormat)
        self.lblTrackDuration.set_text(self.CurrentDurationFormat)
        self.pbarCurrentPosition.set_current_progress(self.CurrentPositionPercent)
        
        self.Play()
        
    def updateCurrentPosition(self):
        self.CurrentPosition = self.getAdjustedCurrentPosition()
        self.CurrentPositionPercent = (self.CurrentPosition/self.CurrentDurationSeconds) * 100
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition )
        self.window_surface.blit(self.background, (2, 178))
        self.lblCurrentPosition.set_text(self.CurrentPositionFormat)
        self.pbarCurrentPosition.set_current_progress(self.CurrentPositionPercent)
        self.updateCurrentTrack(self.CurrentTrackId,  self.CurrentPosition)

    def resetCurrentPosition(self):
        self.CurrentPosition = 0
        self.CurrentPositionPercent = 0
        self.StartPlaybackPosition = 0
        self.CurrentPositionFormat = '00:00'
        self.updateCurrentTrack(self.CurrentTrackId,  self.CurrentPosition)
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition )
        self.window_surface.blit(self.background, (2, 178))
        self.lblCurrentPosition.set_text(self.CurrentPositionFormat)
        self.manager.draw_ui(self.window_surface)
        self.lblCurrentPosition.rebuild()
        self.updateCurrentTrack(self.CurrentTrackId,  self.CurrentPosition)
        
    def MusicScreen(self):
        self.bPlaylists = UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                                 text='Playlists',
                                                 container = self.windowMusic,
                                                 manager=self.manager, 
                                                 object_id=ObjectID(class_id='@navigation_buttons'))
        
        self.bAlbums = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                                text='Albums',
                                                container = self.windowMusic,
                                                manager=self.manager, 
                                                object_id=ObjectID(class_id='@navigation_buttons'))
                                                       
        self.bArtists = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                               text='Artists',
                                               container = self.windowMusic,
                                               manager=self.manager, 
                                               object_id=ObjectID(class_id='@navigation_buttons')) 
                                            
        self.bGenres = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                                text='Genres',
                                                container = self.windowMusic,
                                                manager=self.manager, 
                                                object_id=ObjectID(class_id='@navigation_buttons'))
        self.MusicScreenInit = True
        return

    def MusicScreenHide(self):
         self.windowMusic.hide()

    def MusicScreenShow(self):
         if self.MusicScreenInit == False:
            self.MusicScreen()
         self.windowMusic.show()
        
    def getAvailablePlaylists(self):
        dfDownloadedPlaylists = self.getDownloadedPlaylists()[['PlaylistId','Playlist']]
        return dfDownloadedPlaylists
        
    def getPlaylistTracks(self,  PlaylistId):
        sPlaylistId = PlaylistId
        dfTracks = self.getPlaylistTracksFromDB(sPlaylistId)
        return dfTracks
    
#    def getNextPlaylistIdTrackId(self):
#        return self.getNextPlaylistIdTrackId()
     
    def setNextTrack(self):
        sNextPlaylistId, sNextTrack = self.getNextPlaylistIdTrackId()
        if sNextPlaylistId != self.NextPlaylistId:
            self.NextPlaylistId = sNextPlaylistId
        self.NextTrackId = sNextTrack
        
#    def getPreviousPlaylistIdTrackId(self):
#        return self.getPreviousPlaylistIdTrackId()
        
    def setPreviousTrack(self):
        print(f'CurrentScreen:{self.CurrentScreen}')
        sNextPlaylistId, sNextTrack = self.getPreviousPlaylistIdTrackId()
        if sNextPlaylistId != self.NextPlaylistId:
            self.NextPlaylistId = sNextPlaylistId
        self.NextTrackId = sNextTrack
        
    def AvailablePlaylistsScreen(self):
        self.sPlaylistSelectionList = UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = '',  #playlists,
                                                                                                       container = self.windowAvailablePlaylists,
                                                                                                       manager=self.manager,
                                                                                                       object_id=ObjectID(class_id='@navigation_buttons'), 
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)
        self.AvailablePlaylistsScreenInit = True
        
    def AvailablePlaylistsScreenHide(self):
         self.windowAvailablePlaylists.hide()

    def AvailablePlaylistsScreenShow(self):
        dfAvailablePlaylists = self.getDownloadedPlaylists()
        self.sPlaylistSelectionList.set_item_list(list(dfAvailablePlaylists['Playlist']))
        self.setUISelectionListButtonTheme(self.sPlaylistSelectionList,  '@navigation_buttons')
        self.windowAvailablePlaylists.show()

    def PlaylistTracksScreen(self): 
        self.sPlaylistTracks= UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = '', #list(dfPlaylistTracks['Title']), 
                                                                                                       container = self.windowPlaylistTracks,
                                                                                                       manager=self.manager, 
                                                                                                       object_id=ObjectID(class_id='@navigation_buttons'),
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)

        
    def PlaylistTracksScreenHide(self):
        self.windowPlaylistTracks.hide()
        
    def setUISelectionListButtonTheme(self,  UISelectionList,  Theme):
        for element in UISelectionList.item_list_container:
            element.change_object_id(Theme)

            
    def PlaylistTracksScreenShow(self):
        dfPlaylistTracks = self.getCurrentPlaylist()
        print(f'list(dfPlaylistTracks["Title"]): {list(dfPlaylistTracks["Title"])}')
        self.sPlaylistTracks.set_item_list(list(dfPlaylistTracks['Title']))
        self.setUISelectionListButtonTheme(self.sPlaylistTracks,  '@navigation_buttons')
        self.windowPlaylistTracks.show()

    def getAdjustedCurrentPosition(self):
        currentPosition = round(self.getCurrentPosition())
        if currentPosition >= self.CurrentDurationSeconds:
            return self.CurrentDurationSeconds
        else:
            return currentPosition + self.StartPlaybackPosition
        
    def getCurrentDuration(self):
        return self.CurrentDurationSeconds
    
    def show(self, ScreenName):
        match ScreenName:
            case 'AvailablePlaylists':
                self.AvailablePlaylistsScreenShow()
            case 'Main':
                self.MainScreenShow()
            case 'Music':
                self.MusicScreenShow()
            case 'NowPlaying':
                self.NowPlayingScreenShow()
            case 'PlaylistTracks':
                self.PlaylistTracksScreenShow()
            case _:
                pass

    def hide(self, ScreenName):
        match ScreenName:
            case 'AvailablePlaylists':
                self.AvailablePlaylistsScreenHide()
            case 'Main':
                self.MainScreenHide()
            case 'Music':
                self.MusicScreenHide()
            case 'NowPlaying':
                self.NowPlayingScreenHide()
            case 'PlaylistTracks':
                self.PlaylistTracksScreenHide()
            case _:
                pass
