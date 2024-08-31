import os
import time
import datetime

import pygame
import pygame_gui
#from pygame.font import Font
from pygame_gui.core import ObjectID
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
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage
from pygame_gui.ui_manager import UIManager

#pygame.init()

#class pygame_event_get(pygame.event.get):
#    def  __init__(self):
#        
#        super(pygame.error).__init__()
#        super(pygame.event.get).__init__()
#    pass
#    
class piPodGUI():
    def __init__(self):
#        super(pygame_event_get).__init__()
#        super(pygame_gui.ui_manager).__init__()
#        super(pygame_gui).__init__()
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('piPod')
        
        self.configuration = piPodConfiguration()
        themeFile =os.path.join(self.configuration.ThemeDirectory,  self.configuration.ThemeFile)

        self.window_surface = pygame.display.set_mode((320,240))
        self.background = pygame.Surface((320,240))
        self.background.fill(pygame.Color('aquamarine1'))
        self.manager = pygame_gui.UIManager((320,240),  themeFile)
       
        self.piPodAudio = AudioPlayback()
        self.musicDB = MusicDB()     
        self.containerMainWindow = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager)
        self.containerNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
        self.containerPlay = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
        self.containerPause = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
        self.containerMusic = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
        self.containerAvailablePlaylists = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
        self.containerPlaylistTracks = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
        self.containerPause= pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
#        self.containerCurrentPosition = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 0)
        
        self.SelectedPlaylistName = None
        self.SelectedPlaylistId = None
        self.SelectedTrackTitle = None
        self.SelectedTrackTitleId = None
        

        self.NoAblumArtFile = os.path.join(self.configuration.ImageDirectory,  self.configuration.NoAlbumArt)
#        print(self.NoAblumArtFile)
        self.ImageNoAblumArt = pygame.image.load(self.NoAblumArtFile)
        self.CurrentAlbumArt = self.ImageNoAblumArt
        self.CurrentTitle = ''
        self.CurrentArtist = ''
        self.CurrentAlbum = ''
        self.CurrentGenre = ''
        self.CurrentPlaylist = ''
        self.CurrentDurationSeconds = 0
        self.CurrentDurationFormat = '00:00:00'
        
        self.CurrentPlayState = None
        
        self.MainScreen()
        self.MusicScreen()
        self.AvailablePlaylistsScreen()
        self.PlaylistTracksScreen()
        self.NowPlayingScreen()
#        self.Play()
#        self.Pause()
        
        self.QUIT = pygame.QUIT
        self.UI_BUTTON_PRESSED = pygame_gui.UI_BUTTON_PRESSED
        self.UI_SELECTION_LIST_NEW_SELECTION = pygame_gui.UI_SELECTION_LIST_NEW_SELECTION
        
        
#        
#        self.nowPlayingImage = None
#        self.MainScreen()
#        self.NowPlaying()
#        self.Music()
        
    
#    def setNowPlayingImage(self, NowPlayingArtwork):
#        self.nowPlayingImage = pygame.image.load(imagePath)
#    print(image.get_rect())
    # image = pygame.transform.scale(image, (150, 150))
#    return image

    def button(self, displayText,  left,  top,  width,  height, displayContainer,  displayManager  ):
        btn = UIButton(relative_rect=pygame.Rect((left, top), (width, height)),
                                 text=displayText,
                                 container = displayContainer,
                                 manager = displayManager)
        return btn
    
    def getClock(self):
        return pygame.time.Clock()
      
    def getEvent(self):
        return pygame.event.get()
        
    def updateDisplay(self):
        pygame.display.update()
        
    def quit(self):
        pygame.quit()
    
    def drawScreen(self):
        self.manager.draw_ui(self.window_surface)
      
    def MainScreen(self):
#        self.bNowPlaying = self.button('Now Playing',  12, 30,  300, 24,  self.containerMainWindow,  self.manager)
#        print(type(self.bNowPlaying))
#        self.manager.set_ui_theme( self.piPodTheme)
        self.bNowPlaying = UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                                       text='Now Playing',
                                                       container = self.containerMainWindow,
                                                       manager = self.manager)
    
        self.bMusic = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                             text='Music',
                                             container = self.containerMainWindow,
                                             manager=self.manager)

        self.bOTR = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                           text='OTR',
                                           container = self.containerMainWindow,
                                           manager=self.manager)

        self.bAudiobooks = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                                      text='Audiobooks',
                                                      container = self.containerMainWindow,
                                                      manager=self.manager)

        self.bGames = UIButton(relative_rect=pygame.Rect((12, 120), (300, 24)),
                                               text='Games',
                                               container = self.containerMainWindow,
                                               manager=self.manager)

        self.bManagement = UIButton(relative_rect=pygame.Rect((12, 150), (300, 24)),
                                                         text='Mangement',
                                                         container = self.containerMainWindow,
                                                         manager=self.manager)

        self.containerMainWindow.add_element(self.bNowPlaying) 
        self.containerMainWindow.add_element(self.bMusic)
        self.containerMainWindow.add_element(self.bOTR)
        self.containerMainWindow.add_element(self.bAudiobooks)
        self.containerMainWindow.add_element(self.bGames)
        self.containerMainWindow.add_element(self.bManagement)
        self.window_surface.blit(self.background, (0, 0))
##        self.updateDisplay()
##        
#        self.manager.draw_ui(self.window_surface)
#        pygame.display.flip()
    
#        return #bNowPlaying, bMusic, bOTR, bAudiobooks, bGames, bManagement
    
    def HideMainScreen(self):
        self.containerMainWindow.hide()

    def ShowMainScreen(self):
        self.containerMainWindow.show()
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
                                                   container = self.containerNowPlaying,
                                                   manager=self.manager, 
                                                   object_id=ObjectID(class_id='@now_playing_labels'))
        self.lblTrackArtist = UILabel(relative_rect=pygame.Rect((177,25 ), (120, 21)),
                                                     text = self.CurrentArtist, 
                                                     container = self.containerNowPlaying,
                                                     manager=self.manager, 
                                                     object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.lblTrackAlbum = UILabel(relative_rect=pygame.Rect((177,45 ), (120, 21)),
                                                       text = self.CurrentAlbum,
                                                       container = self.containerNowPlaying,
                                                       manager=self.manager, 
                                                       object_id=ObjectID(class_id='@now_playing_labels'))
                        
        self.lblTrackGenre = UILabel(relative_rect=pygame.Rect((177,65 ), (120, 21)),
                                                      text = self.CurrentGenre,
                                                      container = self.containerNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.lblTrackPlaylist = UILabel(relative_rect=pygame.Rect((177, 85), (120, 21)),
                                                        text = self.CurrentPlaylist , 
                                                        container = self.containerNowPlaying,
                                                        manager=self.manager, 
                                                        object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.imgAlbumArt = UIImage(relative_rect=pygame.Rect((10, 0 ), (128, 128)),
                                                       image_surface=self.CurrentAlbumArt, 
                                                       container = self.containerNowPlaying,
                                                       manager=self.manager)
                                                       
        self.bPlay = UIButton(relative_rect=pygame.Rect((210, 120 ), (50, 50)),
                                                      text='Play',
                                                      container = self.containerPlay,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#play_button'))
                                                                                      
        self.bPause = UIButton(relative_rect=pygame.Rect((210, 120 ), (50, 50)),
                                                      text='Pause',
                                                      container = self.containerPause,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#pause_button'))   
                                                                                      
        self.pbarCurrentPosition = UIProgressBar(relative_rect=pygame.Rect((58, 180), (210, 15)),
                                                                          container = self.containerNowPlaying,
                                                                          manager=self.manager)
                                                                                                       
        self.lblCurrentPosition = UILabel(relative_rect=pygame.Rect((2, 178), (56, 20)),
                                                            text='00:00:00',
                                                            container = self.containerNowPlaying,
                                                            manager=self.manager, 
                                                            object_id=ObjectID(class_id='@now_playing_labels'))
        
        self.lblTrackDuration = UILabel(relative_rect=pygame.Rect((263, 178), (56, 20)),
                                                            text=self.CurrentDurationFormat,
                                                            container = self.containerNowPlaying,
                                                            manager=self.manager, 
                                                            object_id=ObjectID(class_id='@now_playing_labels'))
   
        self.containerNowPlaying.add_element(self.imgAlbumArt)
        self.containerNowPlaying.add_element(self.lblTrackTitle)
        self.containerNowPlaying.add_element(self.lblTrackArtist)
        self.containerNowPlaying.add_element(self.lblTrackAlbum)
        self.containerNowPlaying.add_element(self.lblTrackGenre)
        self.containerNowPlaying.add_element(self.lblTrackPlaylist)
        self.containerNowPlaying.add_element(self.pbarCurrentPosition) 
        
#        self.CurrentPositionLabel()
        
        self.containerPlay.add_element(self.bPlay)
        self.containerPause.add_element(self.bPause)
        self.containerPause.hide()
        
        return self.containerNowPlaying,  self.containerPlay,   self.containerPause # self.piPodAudio
    
#    def CurrentPositionLabel(self, CurrentPosition = '00:00:00'):
#        self.lblCurrentPosition = UILabel(relative_rect=pygame.Rect((2, 178), (56, 20)),
#                                                            text=CurrentPosition,
#                                                            container = self.containerCurrentPosition,
#                                                            manager=self.manager, 
#                                                            object_id=ObjectID(class_id='@now_playing_labels'))
#        self.containerCurrentPosition.add_element(self.lblCurrentPosition)
#        self.containerCurrentPosition.show()
#        pygame.display.flip()
        
    def HideNowPlayingScreen(self):
        self.containerNowPlaying.hide()
        # btnAlbumArt.hide()
        
    def Play(self):
        self.containerPause.kill()
        self.containerPlay = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 1)
        self.bPlay = UIButton(relative_rect=pygame.Rect((210, 120 ), (50, 50)),
                                                      text='',
                                                      container = self.containerPlay,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#play_button'))
                                                                                      
        self.containerPlay.add_element(self.bPlay)
        
    def Pause(self):
        self.containerPlay.kill()
        self.containerPause= pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 1)
        self.bPause = UIButton(relative_rect=pygame.Rect((210, 120 ), (50, 50)),
                                                      text='',
                                                      container = self.containerPause,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#pause_button'))
        self.containerPause.add_element(self.bPause)
       
    def ShowNowPlayingScreen(self, SelectedPlaylistId, SelectedTrackId):
#        self.manager.set_ui_theme( self.piPodTheme)
        self.SelectedPlaylistId = SelectedPlaylistId
        self.SelectedTrackId = SelectedTrackId
        self.window_surface.blit(self.background, (0, 0))
#        dfTrack = self.musicDB.getTrackFromDB(self.SelectedTrackId)
#        sCurrentTrackFile = os.path.join(dfTrack['FileLocation'].iloc[0],  dfTrack['FileName'].iloc[0])
#        currentTrack = self.piPodAudio.setTrack(sCurrentTrackFile)
        currentTrackID3 = self.piPodAudio.getTrackID3Tags(self.SelectedTrackId)
        currentPlaylist = self.musicDB.getPlaylistInfoFromDB(SelectedPlaylistId)
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
        self.CurrentDurationFormat = str(datetime.timedelta(seconds=self.CurrentDurationSeconds))
        
        
        self.musicDB.setNowPlayingPlaylist(self.SelectedPlaylistId ,  self.SelectedTrackId)
        self.musicDB.setNowPlayingTrack( self.SelectedTrackId,  self.CurrentDurationSeconds,  0, 0)
        self.containerNowPlaying.kill()
        pygame.display.flip()
        self.containerNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 1)
        self.NowPlayingScreen()
        self.Play()

    def updateCurrentPosition(self,  CurrentPosition,  TimeDelta):
#        time.sleep(1)
        sCurrentPosition = str(datetime.timedelta(seconds=round(CurrentPosition)))
        self.window_surface.blit(self.background, (2, 178))
        self.lblCurrentPosition.set_text(sCurrentPosition)
        print(type(self.lblCurrentPosition))
        self.manager.draw_ui(self.window_surface)
        self.lblCurrentPosition.rebuild()
#        self.lblCurrentPosition.set_text('')
        self.lblCurrentPosition.update(TimeDelta)
#        pygame.display.flip()
#        self.lblCurrentPosition.set_text(str(sCurrentPosition))
#        self.lblCurrentPosition.update(TimeDelta)
#        self.lblCurrentPosition.update(TimeDelta)
#        pygame.display.flip()
        
    def MusicScreen(self):
#        self.manager.set_ui_theme( self.piPodTheme)
        self.bPlaylists = UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                            text='Playlists',
                                            container = self.containerMusic,
                                            manager=self.manager)
        
        self.bAlbums = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                                text='Albums',
                                                container = self.containerMusic,
                                            manager=self.manager)
        self.bArtists = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                              text='Artists',
                                              container = self.containerMusic,
                                              manager=self.manager) 
                                            
        self.bGenres = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                               text='Genres',
                                               container = self.containerMusic,
                                               manager=self.manager)
        
        self.containerMusic.add_element(self.bPlaylists)
        self.containerMusic.add_element(self.bAlbums)
        self.containerMusic.add_element(self.bArtists)
        self.containerMusic.add_element(self.bGenres)
        return self.containerMusic

    def HideMusicScreen(self):
         self.containerMusic.hide()
        # btnAlbumArt.hide()


    def ShowMusicScreen(self):
         self.containerMusic.show()
        
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
        
    def AvailablePlaylistsScreen(self):
#        self.manager.set_ui_theme( self.piPodTheme)
        self.sPlaylistSelectionList = UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = list(self.getAvailablePlaylists()['Playlist']), 
                                                                                                       container = self.containerAvailablePlaylists,
                                                                                                       manager=self.manager, 
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)
        self.containerAvailablePlaylists.add_element(self.sPlaylistSelectionList)
        return self.containerAvailablePlaylists
        
    def HideAvailablePlaylistsScreen(self):
         self.containerAvailablePlaylists.hide()
        # btnAlbumArt.hide()

    def ShowAvailablePlaylistsScreen(self):
        self.sPlaylistSelectionList.set_item_list(list(self.getAvailablePlaylists()['Playlist']))
        self.containerAvailablePlaylists.show()

        
    def SelectedPlaylistTracks(self,  SelectedNowPlayingPlaylistId,  SelectedNowPlayingPlaylistName):
        self.SelectedPlaylistId = SelectedNowPlayingPlaylistId
        self.SelectedPlaylistName = SelectedNowPlayingPlaylistName
#        dfAvailablePlaylists = self.getAvailablePlaylists()
#        sPlaylistID = dfAvailablePlaylists[dfAvailablePlaylists['Playlist'] == SelectedPlaylistName]['PlaylistId']
        dfTracks = self.getPlaylistTracks(self.SelectedPlaylistName)
        return dfTracks
        
    def PlaylistTracksScreen(self): # ,  SelectedPlaylistId):
#        sSelectedPlaylistName = SelectedPlaylistName
#        dfPlaylistTracks = self.getPlaylistTracks(SelectedPlaylistId)
        self.sPlaylistTracks= UISelectionList(relative_rect=pygame.Rect((12, 0), (300, 220)),
                                                                                                       item_list = [], #list(dfPlaylistTracks['Title']), 
                                                                                                       container = self.containerAvailablePlaylists,
                                                                                                       manager=self.manager, 
#                                                                                                       allow_multi_select=False,
                                                                                                       allow_double_clicks=False)
        self.containerPlaylistTracks.add_element(self.sPlaylistTracks)
        return self.containerPlaylistTracks
        
    def HidePlaylistTracksScreen(self):
        self.containerPlaylistTracks.hide()
        self.background.fill(pygame.Color('aquamarine1'))
        # btnAlbumArt.hide()

    def ShowPlaylistTracksScreen(self,  SelectedPlaylistId):
        dfPlaylistTracks = self.getPlaylistTracks(SelectedPlaylistId)
        self.sPlaylistTracks.set_item_list(list(dfPlaylistTracks['Title']))
        self.containerPlaylistTracks.show()

    def getCurrentPosition(self):
        return self.piPodAudio.getCurrentPosition()
        
    def getCurrentDuration(self):
        return self.piPodAudio.CurrentDuration
