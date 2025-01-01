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
   
class piPodGUI(AudioPlayback):
    def __init__(self):
        super().__init__()
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
        self.musicDB = MusicDB()
        
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
        
        self.CurrentPlaylistId = self.musicDB.getCurrentPlaylistId()
        self.CurrentPlaylistInfo = self.musicDB.getCurrentPlaylistInfo()
            
        self.CurrentTrackId = self.musicDB.getCurrentTrackId()
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
        
        
#        pygame.display.update()
#        pygame.display.flip()
#        self.Play()
#        self.Pause()
        
        self.QUIT = pygame.QUIT
        self.UI_BUTTON_PRESSED = pygame_gui.UI_BUTTON_PRESSED
        self.UI_SELECTION_LIST_NEW_SELECTION = pygame_gui.UI_SELECTION_LIST_NEW_SELECTION
#        self.Screens = self.configuration.Screens
#        self.ScreenNavigation = self.configuration.ScreenNavigation
#        self.ScreenNavigation['AvailablePlaylists'] = []
#        print(f'self.ScreenNavigation: {self.ScreenNavigation}')
#        self.CurrentScreen = self.configuration.DefaultScreen
#        self.CurrentScreenElement = self.configuration.DefaultElement
#        self.PreviousScreen = self.configuration.DefaultScreen
#        self.PreviousScreenElement = self.configuration.DefaultElement
        
        
#        self.MUSICENDEVENT = self.piPodAudio.MUSICENDEVENT
#        print('self.UI_BUTTON_PRESSED:',  self.UI_BUTTON_PRESSED)
#        print('self.UI_SELECTION_LIST_NEW_SELECTION:',  self.UI_SELECTION_LIST_NEW_SELECTION)
#        print('self.MUSIC_END:',  self.MUSIC_END)
    
    def getClock(self):
        return pygame.time.Clock()
      
    def getEvent(self):
        events = pygame.event.get()
#        for event in events:
#            print('event:',  event.type)
#            match event.type:
#                case self.QUIT:
#                    print('quit')
#                case self.UI_BUTTON_PRESSED: 
#                    print('button pressed')
#                case self.UI_SELECTION_LIST_NEW_SELECTION:
#                    print('selection')
#                case self.MUSICENDEVENT:
#                    print('song end')
#                case _:
#                    pass
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
      
    def MainScreen(self):
#        self.bNowPlaying = self.button('Now Playing',  12, 30,  300, 24,  self.containerMainWindow,  self.manager)
#        print(type(self.bNowPlaying))
#        self.manager.set_ui_theme( self.piPodTheme)
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

#        self.containerMainWindow.add_element(self.bNowPlaying) 
#        self.containerMainWindow.add_element(self.bMusic)
#        self.containerMainWindow.add_element(self.bOTR)
#        self.containerMainWindow.add_element(self.bAudiobooks)
#        self.containerMainWindow.add_element(self.bGames)
#        self.containerMainWindow.add_element(self.bManagement)
        self.window_surface.blit(self.background, (0, 0))
##        self.updateDisplay()
##        
#        self.manager.draw_ui(self.window_surface)
#        pygame.display.flip()
    
#        return #bNowPlaying, bMusic, bOTR, bAudiobooks, bGames, bManagement
    
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
#        self.SelectedPlaylistId = SelectedPlaylistId
#        self.SelectedTrackId = SelectedTrackId
#        dfTrack = self.musicDB.getTrackFromDB(self.SelectedTrackId)
        
#        sCurrentTrackFile = os.path.join(dfTrack['FileLocation'].iloc[0],  dfTrack['FileName'].iloc[0])
#        currentTrack = self.piPodAudio.setTrack(sCurrentTrackFile)
#        print(currentTrack['title'])
#        sCurrentTitle = str(currentTrack['title'])
#        print(type(sCurrentTitle))
#        self.manager.set_ui_theme(self.piPodTheme)
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
        self.bRepeatOn.hide()
        self.bRepeatOne.hide()
        self.bRepeatOff.show()
        self.bRepeatOff.select()
        self.bRepeatOff.unselect()
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
        
    def RepeatOff(self):
        self.Repeat = 'Off'
        self.ShowRepeatButtonOff()
        
    def RepeatOn(self):
        self.Repeat = 'On'
        self.ShowRepeatButtonOn()
        
    def RepeatOne(self):
        self.Repeat = 'One'
        self.ShowRepeatButtonOne()
        
    def setCurrentPlaylist(self, PlaylistId):
        self.CurrentPlaylistId = PlaylistId
        
#        CurrentTrackId = TrackId
        self.musicDB.setCurrentPlaylist(self.CurrentPlaylistId)
        self.CurrentPlaylistInfo = self.musicDB.getCurrentPlaylistInfo()
        
    def setCurrentTrack(self, TrackId):
        self.CurrentTrackId = TrackId
        dfTrack = self.musicDB.getTrackFromDB(self.CurrentTrackId)
        CurrentDurationSeconds = dfTrack['DurationSeconds'][0].item()
        self.musicDB.setCurrentTrack(self.CurrentTrackId, CurrentDurationSeconds)
        
    def NowPlayingScreenShow(self):
        dfCurrentTrack = self.musicDB.getCurrentTrack()
        self.CurrentTrackId = dfCurrentTrack['TrackId'][0]
        self.StartPlaybackPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition)
#        print(self.CurrentPosition)
#        print(self.CurrentPositionFormat)
        
        currentTrackID3 = self.getTrackID3Tags(self.CurrentTrackId)
        currentPlaylist = self.musicDB.getPlaylistInfoFromDB(self.CurrentPlaylistId)
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
        
#        self.musicDB.setNowPlayingPlaylist(self.CurrentPlaylistId ,  self.CurrentTrackId)
#        self.musicDB.setNowPlayingTrack( self.CurrentTrackId,  self.CurrentDurationSeconds,  0, 0)
#        self.containerNowPlaying.kill()
        pygame.display.flip()
#        self.containerNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 1)
#        self.NowPlayingScreen()
#        pygame.display.flip()
        if self.AutoPlayOnStart:
            self.Play()
        else:
            self.Pause()
            
    def NextTrackNowPlaying(self):
        if self.Repeat == 'One':
            # Repeat Track is on.  Set the starting position to 0 and start the track
#            self.NextPlaylistId = self.CurrentPlaylistId
#            self.NextTrackId = self.CurrentTrackId
            self.StartPlaybackPosition = 0
            self.setTrack(self.CurrentTrackId,  0)
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
            dfFirstTrack = self.musicDB.getFirstTrack(self.CurrentPlaylistId)
            self.NextTrackId = dfFirstTrack['TrackId'][0]
#        self.musicDB.setCurrentPlaylist(self.NextPlaylistId)
#        self.CurrentPlaylistId = self.NextPlaylistId
        self.musicDB.setCurrentTrack(self.NextTrackId)
        dfCurrentTrack = self.musicDB.getCurrentTrack()
        self.CurrentTrackId = dfCurrentTrack['TrackId'][0]
        self.StartPlaybackPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition)
        currentTrackID3 = self.getTrackID3Tags(self.CurrentTrackId)
        currentPlaylist = self.musicDB.getPlaylistInfoFromDB(self.CurrentPlaylistId)
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
            self.musicDB.setCurrentPlaylist(self.NextPlaylistId)
            self.CurrentPlaylistId = self.NextPlaylistId
        
        self.musicDB.setCurrentTrack(self.NextTrackId)
        self.CurrentTrackid = self.NextTrackId
        
        dfCurrentTrack = self.musicDB.getCurrentTrack()
        self.CurrentTrackId = dfCurrentTrack['TrackId'][0]
        self.StartPlaybackPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPosition = dfCurrentTrack['CurrentPosition'][0].item()
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition)
        currentTrackID3 = self.getTrackID3Tags(self.CurrentTrackId)
        currentPlaylist = self.musicDB.getPlaylistInfoFromDB(self.CurrentPlaylistId)
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
#        self.manager.draw_ui(self.window_surface)
#        self.lblCurrentPosition.rebuild()
#        self.lblCurrentPosition.update(TimeDelta)
        self.musicDB.updateCurrentTrack(self.CurrentTrackId,  self.CurrentPosition)

    def resetCurrentPosition(self):
        self.CurrentPosition = 0
        self.CurrentPositionPercent = 0
        self.StartPlaybackPosition = 0
        self.CurrentPositionFormat = '00:00'
        self.musicDB.updateCurrentTrack(self.CurrentTrackId,  self.CurrentPosition)
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition )
        self.window_surface.blit(self.background, (2, 178))
        self.lblCurrentPosition.set_text(self.CurrentPositionFormat)
        self.manager.draw_ui(self.window_surface)
        self.lblCurrentPosition.rebuild()
#        self.lblCurrentPosition.update(TimeDelta)
        self.musicDB.updateCurrentTrack(self.CurrentTrackId,  self.CurrentPosition)
        
    def MusicScreen(self):
#        self.manager.set_ui_theme( self.piPodTheme)
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
#        self.containerMusic.add_element(self.bPlaylists)
#        self.containerMusic.add_element(self.bAlbums)
#        self.containerMusic.add_element(self.bArtists)
#        self.containerMusic.add_element(self.bGenres)
        return

    def MusicScreenHide(self):
         self.windowMusic.hide()
        # btnAlbumArt.hide()


    def MusicScreenShow(self):
         if self.MusicScreenInit == False:
            self.MusicScreen()
         self.windowMusic.show()
        
    def getAvailablePlaylists(self):
        dfDownloadedPlaylists = self.musicDB.getDownloadedPlaylists()[['PlaylistId','Playlist']]
        return dfDownloadedPlaylists
        
    def getPlaylistTracks(self,  PlaylistId):
        sPlaylistId = PlaylistId
#        playlist = self.getAvailablePlaylists()
#        playlistId = playlist[playlist['Playlist'] == PlaylistName]['PlaylistId']
#        playlistId = playlistId.iloc[0]
#        playlistId = self.musicDB.getPlaylistIdbyNamefromDB(sPlaylistName)
        dfTracks = self.musicDB.getPlaylistTracksFromDB(sPlaylistId) #['TrackdId',  'Title']
        return dfTracks
    
    def getNextPlaylistIdTrackId(self):
        return self.musicDB.getNextPlaylistIdTrackId()
     
    def setNextTrack(self):
        sNextPlaylistId, sNextTrack = self.getNextPlaylistIdTrackId()
        if sNextPlaylistId != self.NextPlaylistId:
            self.NextPlaylistId = sNextPlaylistId
        self.NextTrackId = sNextTrack
        
    def getPreviousPlaylistIdTrackId(self):
        return self.musicDB.getPreviousPlaylistIdTrackId()
        
    def setPreviousTrack(self):
        print(f'CurrentScreen:{self.CurrentScreen}')
        sNextPlaylistId, sNextTrack = self.getPreviousPlaylistIdTrackId()
        if sNextPlaylistId != self.NextPlaylistId:
            self.NextPlaylistId = sNextPlaylistId
        self.NextTrackId = sNextTrack
        
    def AvailablePlaylistsScreen(self):
#        if self.AvailablePlaylistsScreenInit == False:
#            self.AvailablePlaylistsScreen()
#        self.manager.set_ui_theme( self.piPodTheme)
#        playlists = list(self.getAvailablePlaylists()['Playlist'])
#        self.ScreenNavigation['AvailablePlaylists'] = playlists
        self.sPlaylistSelectionList = UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = '',  #playlists,
                                                                                                       container = self.windowAvailablePlaylists,
                                                                                                       manager=self.manager,
#                                                                                                       object_id=ObjectID(class_id='@navigation_buttons'), 
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)
        self.AvailablePlaylistsScreenInit = True
#        self.containerAvailablePlaylists.add_element(self.sPlaylistSelectionList)
#        return self.containerAvailablePlaylists
        
    def AvailablePlaylistsScreenHide(self):
         self.windowAvailablePlaylists.hide()
        # btnAlbumArt.hide()

    def AvailablePlaylistsScreenShow(self):
        dfAvailablePlaylists = self.musicDB.getDownloadedPlaylists()
        self.sPlaylistSelectionList.set_item_list(list(dfAvailablePlaylists['Playlist']))
        self.setUISelectionListButtonTheme(self.sPlaylistSelectionList,  '@navigation_buttons')
#        IndexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)        
        self.windowAvailablePlaylists.show()
        
#        self.setSelectionListItemSelected(self.sPlaylistSelectionList, IndexCurrentElement)

        
#    def SelectedPlaylistTracks(self,  SelectedNowPlayingPlaylistId,  SelectedNowPlayingPlaylistName):
#        self.SelectedPlaylistId = SelectedNowPlayingPlaylistId
#        self.SelectedPlaylistName = SelectedNowPlayingPlaylistName
#        dfTracks = self.getPlaylistTracks(self.SelectedPlaylistName)
#        return dfTracks
        #
    def PlaylistTracksScreen(self): # ,  SelectedPlaylistId):
#        sSelectedPlaylistName = SelectedPlaylistName
#        dfPlaylistTracks = self.getPlaylistTracks(SelectedPlaylistId)
        self.sPlaylistTracks= UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = '', #list(dfPlaylistTracks['Title']), 
                                                                                                       container = self.windowPlaylistTracks,
                                                                                                       manager=self.manager, 
                                                                                                       object_id=ObjectID(class_id='@navigation_buttons'),
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)
#        self.containerPlaylistTracks.add_element(self.sPlaylistTracks)
#        return self.containerPlaylistTracks
        
    def PlaylistTracksScreenHide(self):
        self.windowPlaylistTracks.hide()
#        self.background.fill(pygame.Color('aquamarine1'))
        # btnAlbumArt.hide()
        
    def setUISelectionListButtonTheme(self,  UISelectionList,  Theme):
#        self.sPlaylistSelectionList.item_list_container.elements[itemIndex].change_object_id('@navigation_buttons')
        for element in UISelectionList.item_list_container:
            element.change_object_id('@navigation_buttons')

            
    def PlaylistTracksScreenShow(self):
        dfPlaylistTracks = self.musicDB.getCurrentPlaylist()
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
                pass#    def setTrack(self,  TrackId):

#    def setCurrentScreen(self,  ScreenName):
#        # Check id Screen is a configured 
#        if ScreenName in self.Screens:
#            self.PreviousScreen = self.CurrentScreen
#            self.CurrentScreen = ScreenName
#        else:
#            print('error setting currentScreen')
#    
#    def setCurrentScreenElement(self,  ScreenName,  ScreenElement):
#        print(f'self.ScreenNavigation: {self.ScreenNavigation}')
#        if ScreenName in self.ScreenNavigation and ScreenElement in self.ScreenNavigation[ScreenName]:
#            self.setCurrentScreen(ScreenName)
#            self.PreviousScreenElement = self.CurrentScreenElement
#            self.CurrentScreenElement = ScreenElement
#        else:
#            print('error setting currentScreenElement')
#            
#    def getScreenElementIndex(self,  Screen,  ScreenElement):
#        indexCurrentElement = self.ScreenNavigation[Screen].index(ScreenElement)
#        return indexCurrentElement
#        
#    def getCurrentScreenElementIndex(self):
#        indexCurrentElement = self.getScreenElementIndex(self.CurrentScreen,  self.CurrentScreenElement)
#        return indexCurrentElement
    
#    def setScreenElementSelected(self,  Element):
#        match self.CurrentScreen:
#            case 'Main':
#                match Element:
#                    case 'NowPlaying':
#                        self.bNowPlaying.select()
#                    case 'Music':
#                        self.bMusic.select()
#                    case 'OTR':
#                        self.bOTR.select()
#                    case 'Audiobooks':
#                        self.bAudiobooks.select()
#                    case 'Games':
#                        self.bGames.select()
#                    case 'Settings':
#                        self.bManagement.select()
#                    case _:
#                        pass
#            case 'NowPlaying':
#                match Element:
#                    case 'Play/Pause':
#                        if self.getAudioPlayingStatus == False:
#                            self.ShowPlayButton()
#                            self.bPlay.select()
#                        else:
#                            self.ShowPauseButton()
#                            self.bPause.select()
#                    case 'Forward':
#                        self.bForward.select()
#                    case 'Back':
#                        self.bBack.select()
#                    case 'Home':
#                        self.bHome.select()
#                    case _:
#                        pass
#            case 'Music':
#                match Element:
#                    case 'AvailablePlaylists':
#                        self.bPlaylists.select()
#                    case 'Albums':
#                        self.bAlbums.select()
#                    case 'Artists':
#                        self.bArtists.select()
#                    case 'Genres':
#                        self.bGenres.select()
#                    case 'Back':
#                        self.bBack.select()
#                    case 'Home':
#                        self.bHome.select()
#                    case _:
#                        pass
#            case'AvailablePlaylists':
#                itemIndex = self.getCurrentScreenElementIndex()
#                self.sPlaylistSelectionList.item_list_container.elements[itemIndex].select()                
#            case'PlaylistTracks':
#                itemIndex=self.getCurrentScreenElementIndex()
#                print(f'itemIndex: {itemIndex}')
#                self.sPlaylistTracks.item_list_container.elements[itemIndex].select()
#            case 'OTR':
#                pass
#            case 'Audiobooks':
#                pass
#            case 'Games':
#                pass
#            case 'Settings':
#                pass
#        self.CurrentScreenElement = Element
#        print(f'NewScreenElement: {self.CurrentScreenElement}')
    
#    def setSelectionListItemSelected(self, UISelectList,  ItemIndex):
#        eventData = {'user_type': pygame_gui.UI_SELECTION_LIST_NEW_SELECTION,  #UI_BUTTON_PRESSED,
#                               'ui_element': self.sPlaylistSelectionList.item_list_container.elements[ItemIndex]
#        }
#        selectListItemEvent = pygame.event.Event(pygame.USEREVENT+1500, eventData)
#        print(f'self.sPlaylistSelectionList.item_list_container.elements[ItemIndex]: {self.sPlaylistSelectionList.item_list_container.elements[ItemIndex]}')
##        for x in self.sPlaylistSelectionList.item_list_container.elements[ItemIndex]:
#        print(f'x: {type(self.sPlaylistSelectionList.item_list_container.elements[ItemIndex])}')
#        print(f'get_single_selection1: {UISelectList.get_single_selection()}')
#        self.manager.process_events(selectListItemEvent)
#        print(f'get_single_selection2: {UISelectList.get_single_selection()}')
#        self.sPlaylistSelectionList.item_list_container.elements[ItemIndex].select()
#        eventData = {'ui_element': UISelectList.item_list_container.elements[ItemIndex]}
#        selectListItemEvent = pygame.event.Event(pygame_gui.UI_SELECTION_LIST_NEW_SELECTION, eventData)
#        UISelectList.process_event(selectListItemEvent)
    
#    def setScreenElementUnselected(self, Element):
#        match self.CurrentScreen:
#            case 'Main':
#                match Element:
#                    case 'NowPlaying':
#                        self.bNowPlaying.unselect()
#                    case 'Music':
#                        self.bMusic.unselect()
#                    case 'OTR':
#                        self.bOTR.unselect()
#                    case 'Audiobooks':
#                        self.bAudiobooks.unselect()
#                    case 'Games':
#                        self.bGames.unselect()
#                    case 'Settings':
#                        self.bManagement.unselect()
#                    case _:
#                        pass
#            case 'NowPlaying':
#                match Element:
#                    case 'Play/Pause':
#                        if self.getAudioPlayingStatus == False:
#                            self.ShowPlayButton()
#                            self.bPlay.unselect()
#                        else:
#                            self.ShowPauseButton()
#                            self.bPause.unselect()
#                    case 'Forward':
#                        self.bForward.unselect()
#                    case 'Back':
#                        self.bBack.unselect()
#                    case 'Home':
#                        self.bHome.unselect()
#                    case _:
#                        pass
#            case 'Music':
#               match Element:
#                    case 'AvailablePlaylists':
#                        self.bPlaylists.unselect()
#                    case 'Albums':
#                        self.bAlbums.unselect()
#                    case 'Artists':
#                        self.bArtists.unselect()
#                    case 'Genres':
#                        self.bGenres.unselect()
#                    case _:
#                        pass
#            case'AvailablePlaylists':
#                itemIndex = self.getCurrentScreenElementIndex()
#                self.sPlaylistSelectionList.item_list_container.elements[itemIndex].unselect()
#            case'PlaylistTracks':
#                itemIndex = self.getCurrentScreenElementIndex()
#                self.sPlaylistTracks.item_list_container.elements[itemIndex].unselect()
#            case 'OTR':
#                pass
#            case 'Audiobooks':
#                pass
#            case 'Games':
#                pass
#            case 'Settings':
#                pass
#    def NavigateUp(self, IndexCurrentElement):
##        lengthScreenNavigation = len(self.ScreenNavigation[self.CurrentScreen]) - 1
#        if IndexCurrentElement  > 0:
#            IndexCurrentElement = self.getCurrentScreenElementIndex()-1
#            self.setScreenElementUnselected(self.CurrentScreenElement)
#            self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
#            self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
##            match self.CurrentScreen:
##                case 'AvailablePlaylists':
##                    IndexCurrentElement = getCurrentScreenElementIndex()-1
##                    self.setScreenElementUnselected(self.CurrentScreenElement)
##                    self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
##                    self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
##                case _:
##                    IndexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)-1
##                    self.setScreenElementUnselected(self.CurrentScreenElement)
##                    self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
##                    self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
#                    
#            print(f'indexCurrentElement: {IndexCurrentElement}')
#        else:
#            pass
#            
#    def NavigateDown(self, IndexCurrentElement):
#        lengthScreenNavigation = len(self.ScreenNavigation[self.CurrentScreen]) - 1
#        
#        if IndexCurrentElement  < lengthScreenNavigation:
#            IndexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)+1
#            self.setScreenElementUnselected(self.CurrentScreenElement)
#            self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
#            self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
##            match self.CurrentScreen:
##                case 'AvailablePlaylists':
##                    IndexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)+1
##                    self.setScreenElementUnselected(self.CurrentScreenElement)
##                    self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
##                    self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
###                    self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
##                case _:
##                    IndexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)+1
##                    self.setScreenElementUnselected(self.CurrentScreenElement)
##                    self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
##                    self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
#            print(f'indexCurrentElement: {IndexCurrentElement}')
#        else:
#            pass
#    def Select(self):
#        match self.CurrentScreen:
#            case 'Main':
#                match self.CurrentScreenElement:
#                    case 'NowPlaying':
#                        self.setCurrentScreenElement('NowPlaying', 'Play/Pause')
#                        self.hide()
#                        self.NowPlayingScreenShow()
#                        self.bPlay.select()
#                    case 'Music':
#                        self.setCurrentScreenElement('Music', 'AvailablePlaylists')
#                        self.MainScreenHide()
#                        self.MusicScreenShow()
#                        self.bPlaylists.select()
#                    case 'OTR':
#                        pass
#                    case 'Audiobooks':
#                        pass
#                    case 'Games':
#                        pass
#                    case 'Settings':
#                        pass
#            case 'NowPlaying':
#                pass
#            case 'Music':
#                match self.CurrentScreenElement:
#                    case 'AvailablePlaylists':
#                        if self.CurrentPlaylistInfo:
#                            playlistIndex = self.getCurrentScreenElementIndex('AvailablePlaylists',  self.CurrentPlaylistInfo[0]['Playlist'])
#                        else:
#                            playlistIndex = 0 
#                        playlists = list(self.getAvailablePlaylists()['Playlist'])
#                        self.ScreenNavigation['AvailablePlaylists'] = playlists
#                        self.setCurrentScreenElement('AvailablePlaylists', playlists[playlistIndex])
#                        self.MusicScreenHide()
#                        self.AvailablePlaylistsScreenShow()
#                    case 'Music':
#                        self.setCurrentScreenElement('Music', 'AvailablePlaylists')
#                        self.MainScreenHide()
#                        self.MusicScreenShow()
#                        self.bPlaylists.select()
#            case 'AvailablePlaylists':
#                selectedPlaylist = self.CurrentScreenElement
#                SelectedNowPlayingPlaylistId = self.musicDB.getPlaylistIdbyNamefromDB(selectedPlaylist)
#                self.setCurrentPlaylist(SelectedNowPlayingPlaylistId)
#                tracks = list(self.getPlaylistTracks(self.CurrentPlaylistId))
##                if 
#                self.ScreenNavigation['PlaylistTracks'] = tracks
##                self.setCurrentScreenElement('AvailablePlaylists', playlists[playlistIndex])
#                self.setCurrentScreenElement('PlaylistTracks', tracks[0])
#                self.AvailablePlaylistsScreenHide()
#                self.PlaylistTracksScreenShow()
#            case 'PlaylistTracks':
#                selectedTrack = self.CurrentScreenElement
#                selectedTrackId = self.musicDB.getTrackIdByNameFromDB(self,  self.CurrentPlaylistId,  TrackName)
#                self.musicDB.setCurrentTrack(selectedTrackId)
#    def EncoderNavigation(self, EncoderActivity):
##        print(f'EncoderActivity: {EncoderActivity}')
##        print(f'CurrentScreenElement: {self.CurrentScreenElement}')
#        control = next(iter(EncoderActivity))
#        controlAction = EncoderActivity[control]
#        indexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)
##        print(f'indexCurrentElement: {indexCurrentElement}') 
#        
##        print(f'lengthScreenNavigation: {lengthScreenNavigation}')
#        match control:
#            case 'Wheel':
#                match controlAction:
#                    case 'Up':
#                        self.NavigateUp(indexCurrentElement)
#                    case 'Down':
#                        self.NavigateDown(indexCurrentElement)
#            case 'Select':
#                match controlAction:
#                    case 'Release':
#                        self.Select()
#                    case 'Press':
#                        pass
#            case 'Up':
#                match controlAction:
#                    case 'Release':
#                        self.NavigateUp(indexCurrentElement)
#                    case 'Press':
#                        pass
#                
#            case 'Down':
#                match controlAction:
#                    case 'Release':
#                        self.NavigateDown(indexCurrentElement)
#                    case 'Press':
#                        pass
#                
#            case 'Left':
#                pass
#                
#            case 'Right':
#                pass
