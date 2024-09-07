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
   
class piPodGUI(AudioPlayback):
    def __init__(self):
        super().__init__()
#        pygame.init()
        pygame.display.set_caption('piPod')
        
        # piPod config file
        self.configuration = piPodConfiguration()
        #pygame_gui Theme file
        themeFile =os.path.join(self.configuration.ThemeDirectory,  self.configuration.ThemeFile)
        
        # pygame_gui setup
        self.window_surface = pygame.display.set_mode((325,245))
        self.background = pygame.Surface((325,245))
        self.background.fill(pygame.Color('aquamarine'))
        self.manager = UIManager((320,240),  themeFile)
       
#        self.piPodAudio = AudioPlayback()
        self.musicDB = MusicDB()
       
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
        self.StartPlaybackPosition = 0
        self.CurrentPositionFormat = '00:00'
        self.CurrentDurationSeconds = 0
        self.CurrentDurationFormat = '00:00'
        
        self.CurrentPlayState = None
        
        self.MainScreen()
        self.MusicScreen()
        self.AvailablePlaylistsScreen()
        self.PlaylistTracksScreen()
        self.NowPlayingScreen()
        
        self.windowMusic.hide()
        self.windowAvailablePlaylists.hide()
        self.windowPlaylistTracks.hide()
        self.windowNowPlaying.hide()
        self.ShowMainScreen()
        
#        pygame.display.update()
#        pygame.display.flip()
#        self.Play()
#        self.Pause()
        
        self.QUIT = pygame.QUIT
        self.UI_BUTTON_PRESSED = pygame_gui.UI_BUTTON_PRESSED
        self.UI_SELECTION_LIST_NEW_SELECTION = pygame_gui.UI_SELECTION_LIST_NEW_SELECTION
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
                                                       object_id=ObjectID(class_id='button'))
    
        self.bMusic = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                             text='Music',
                                             container = self.windowMainScreen, #self.containerMainWindow,
                                             manager=self.manager, 
                                             object_id=ObjectID(class_id='button'))

        self.bOTR = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                           text='OTR',
                                           container = self.windowMainScreen , #self.containerMainWindow,
                                           manager=self.manager, 
                                           object_id=ObjectID(class_id='button'))

        self.bAudiobooks = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                                      text='Audiobooks',
                                                      container = self.windowMainScreen , #self.containerMainWindow,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='button'))

        self.bGames = UIButton(relative_rect=pygame.Rect((12, 120), (300, 24)),
                                               text='Games',
                                               container = self.windowMainScreen , #self.containerMainWindow,
                                               manager=self.manager, 
                                               object_id=ObjectID(class_id='button'))

        self.bManagement = UIButton(relative_rect=pygame.Rect((12, 150), (300, 24)),
                                                         text='Mangement',
                                                         container = self.windowMainScreen , #self.containerMainWindow,
                                                         manager=self.manager, 
                                                         object_id=ObjectID(class_id='button'))

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
    
    def HideMainScreen(self):
        self.windowMainScreen.hide() #self.containerMainWindow.hide()
        self.window_surface.blit(self.background, (0, 0))

    def ShowMainScreen(self):
        if self.CurrentPlaylistId == None or self.CurrentTrackId == None:
            self.bNowPlaying.disable()
        self.windowMainScreen.show() 
        pygame.display.flip()

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
        
        self.pbarCurrentPosition = UIProgressBar(relative_rect=pygame.Rect((58, 180), (210, 15)),
                                                                          container = self.windowNowPlaying,
                                                                          manager=self.manager)
                                                                                                       
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
        
    def HideNowPlayingScreen(self):
        self.windowNowPlaying.hide()
        
    def Play(self):
        if self.CurrentTrackId != None:
            self.bPlay.hide()
            self.bPause.show()
            self.playTrack()
        
    def Pause(self):
        self.pauseTrack()
        self.bPause.hide()
        self.bPlay.show()
        
    def setCurrentPlaylist(self, PlaylistId,):
        self.CurrentPlaylistId = PlaylistId
#        CurrentTrackId = TrackId
        self.musicDB.setCurrentPlaylist(self.CurrentPlaylistId)
    
    def setCurrentTrack(self, TrackId):
        self.CurrentTrackId = TrackId
        dfTrack = self.musicDB.getTrackFromDB(self.CurrentTrackId)
        CurrentDurationSeconds = dfTrack['DurationSeconds'][0].item()
        self.musicDB.setCurrentTrack(self.CurrentTrackId, CurrentDurationSeconds)
        
    def ShowNowPlayingScreen(self):
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
        self.setNextTrack()
        print('NextPlaylistId:',  self.NextPlaylistId)
        print('NextTrackId:',  self.NextTrackId)
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
        
        self.Play()
    def PreviousTrackNowPlaying(self):
        if self.getAdjustedCurrentPosition() >= 5:
            self.rewindTrack()
            self.resetCurrentPosition()
            return
            
        self.setNextTrack()
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
        
        self.Play()
        
    def updateCurrentPosition(self):
        self.CurrentPosition = self.getAdjustedCurrentPosition()
        self.CurrentPositionFormat = self.formatTrackTime(self.CurrentPosition )
        self.window_surface.blit(self.background, (2, 178))
        self.lblCurrentPosition.set_text(self.CurrentPositionFormat)
#        self.manager.draw_ui(self.window_surface)
#        self.lblCurrentPosition.rebuild()
#        self.lblCurrentPosition.update(TimeDelta)
        self.musicDB.updateCurrentTrack(self.CurrentTrackId,  self.CurrentPosition)

    def resetCurrentPosition(self):
        self.CurrentPosition = 0
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
                                            manager=self.manager)
        
        self.bAlbums = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                                text='Albums',
                                                container = self.windowMusic,
                                            manager=self.manager)
        self.bArtists = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                              text='Artists',
                                              container = self.windowMusic,
                                              manager=self.manager) 
                                            
        self.bGenres = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                               text='Genres',
                                               container = self.windowMusic,
                                               manager=self.manager)
        
#        self.containerMusic.add_element(self.bPlaylists)
#        self.containerMusic.add_element(self.bAlbums)
#        self.containerMusic.add_element(self.bArtists)
#        self.containerMusic.add_element(self.bGenres)
        return

    def HideMusicScreen(self):
         self.windowMusic.hide()
        # btnAlbumArt.hide()


    def ShowMusicScreen(self):
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
        
    def AvailablePlaylistsScreen(self):
#        self.manager.set_ui_theme( self.piPodTheme)
        self.sPlaylistSelectionList = UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = list(self.getAvailablePlaylists()['Playlist']), 
                                                                                                       container = self.windowAvailablePlaylists,
                                                                                                       manager=self.manager, 
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)
#        self.containerAvailablePlaylists.add_element(self.sPlaylistSelectionList)
#        return self.containerAvailablePlaylists
        
    def HideAvailablePlaylistsScreen(self):
         self.windowAvailablePlaylists.hide()
        # btnAlbumArt.hide()

    def ShowAvailablePlaylistsScreen(self):
        self.sPlaylistSelectionList.set_item_list(list(self.getAvailablePlaylists()['Playlist']))
        self.windowAvailablePlaylists.show()

        
#    def SelectedPlaylistTracks(self,  SelectedNowPlayingPlaylistId,  SelectedNowPlayingPlaylistName):
#        self.SelectedPlaylistId = SelectedNowPlayingPlaylistId
#        self.SelectedPlaylistName = SelectedNowPlayingPlaylistName
#        dfTracks = self.getPlaylistTracks(self.SelectedPlaylistName)
#        return dfTracks
        
    def PlaylistTracksScreen(self): # ,  SelectedPlaylistId):
#        sSelectedPlaylistName = SelectedPlaylistName
#        dfPlaylistTracks = self.getPlaylistTracks(SelectedPlaylistId)
        self.sPlaylistTracks= UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = [], #list(dfPlaylistTracks['Title']), 
                                                                                                       container = self.windowPlaylistTracks,
                                                                                                       manager=self.manager, 
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)
#        self.containerPlaylistTracks.add_element(self.sPlaylistTracks)
#        return self.containerPlaylistTracks
        
    def HidePlaylistTracksScreen(self):
        self.windowPlaylistTracks.hide()
#        self.background.fill(pygame.Color('aquamarine1'))
        # btnAlbumArt.hide()

    def ShowPlaylistTracksScreen(self):
        dfPlaylistTracks = self.musicDB.getCurrentPlaylist()
        self.sPlaylistTracks.set_item_list(list(dfPlaylistTracks['Title']))
        self.windowPlaylistTracks.show()

    def getAdjustedCurrentPosition(self):
        currentPosition = round(self.getCurrentPosition())
        if currentPosition >= self.CurrentDurationSeconds:
            return self.CurrentDurationSeconds
        else:
            return currentPosition + self.StartPlaybackPosition
        
    def getCurrentDuration(self):
        return self.CurrentDurationSeconds
        
#    def setTrack(self,  TrackId):
