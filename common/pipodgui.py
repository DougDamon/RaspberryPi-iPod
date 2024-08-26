import os
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
#from pygame_gui.ui_manager import UIManager
#from pygame_gui.elements.ui_window import UIWindow
#from pygame_gui.elements.ui_image import UIImage
#from pygame_gui.ui_manager import UIManager

class piPodGUI:
    def __init__(self,  PygameClock,  WindowSurface,  Background,  Manager):
        pygame.init()
        pygame.font.init()
        self.pyGameClock = PygameClock
        self.piPodAudio = AudioPlayback()
        self.musicDB = MusicDB()
        self.configuration = piPodConfiguration()
        self.windowSurface = WindowSurface
        self.background = Background
        self.manager = Manager
        self.containterMainWindow = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager)
        self.containterNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager, visible = 0)
        self.containterMusic = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager, visible = 0)
        self.containerAvailablePlaylists = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager, visible = 0)
        self.containerPlaylistTracks = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager, visible = 0)

        self.SelectedPlaylistName = None
        self.SelectedPlaylistId = None
        self.SelectedTrackTitle = None
        self.SelectedTrackTitleId = None
        
        self.NoAblumArtFile = os.path.join(self.configuration.ImageDirectory,  self.configuration.NoAlbumArt)
        self.ImageNoAblumArt = pygame.image.load(self.NoAblumArtFile)
        self.CurrentAlbumArt = self.ImageNoAblumArt
        self.CurrentTitle = ''
        self.CurrentArtist = ''
        self.CurrentAlbum = ''
        self.CurrentGenre = ''
        self.CurrentPlaylist = ''
        self.CurrentDurationSeconds = 0
        self.CurrentDurationFormat = '00:00:00'
        
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
        
    def MainScreen(self):
#        self.bNowPlaying = self.button('Now Playing',  12, 30,  300, 24,  self.containterMainWindow,  self.manager)
#        print(type(self.bNowPlaying))
        self.bNowPlaying = UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                                       text='Now Playing',
                                                       container = self.containterMainWindow,
                                                       manager = self.manager)
    
        self.bMusic = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                             text='Music',
                                             container = self.containterMainWindow,
                                             manager=self.manager)

        self.bOTR = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                           text='OTR',
                                           container = self.containterMainWindow,
                                           manager=self.manager)

        self.bAudiobooks = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                                      text='Audiobooks',
                                                      container = self.containterMainWindow,
                                                      manager=self.manager)

        self.bGames = UIButton(relative_rect=pygame.Rect((12, 120), (300, 24)),
                                               text='Games',
                                               container = self.containterMainWindow,
                                               manager=self.manager)

        self.bManagement = UIButton(relative_rect=pygame.Rect((12, 150), (300, 24)),
                                                         text='Mangement',
                                                         container = self.containterMainWindow,
                                                         manager=self.manager)

        self.containterMainWindow.add_element(self.bNowPlaying) 
        self.containterMainWindow.add_element(self.bMusic)
        self.containterMainWindow.add_element(self.bOTR)
        self.containterMainWindow.add_element(self.bAudiobooks)
        self.containterMainWindow.add_element(self.bGames)
        self.containterMainWindow.add_element(self.bManagement)
    
#        return #bNowPlaying, bMusic, bOTR, bAudiobooks, bGames, bManagement
    
    def HideMainScreen(self):
        self.containterMainWindow.hide()

    def ShowMainScreen(self):
        self.containterMainWindow.show()

    def NowPlayingScreen(self): #, SelectedPlaylistId,  SelectedTrackId):
#        self.SelectedPlaylistId = SelectedPlaylistId
#        self.SelectedTrackId = SelectedTrackId
#        dfTrack = self.musicDB.getTrackFromDB(self.SelectedTrackId)
        
#        sCurrentTrackFile = os.path.join(dfTrack['FileLocation'].iloc[0],  dfTrack['FileName'].iloc[0])
#        currentTrack = self.piPodAudio.setTrack(sCurrentTrackFile)
#        print(currentTrack['title'])
#        sCurrentTitle = str(currentTrack['title'])
#        print(type(sCurrentTitle))
        self.lblTrackTitle = UILabel(relative_rect=pygame.Rect((177,5 ), (120, 21)),
                                                   text = self.CurrentTitle,
                                                   container = self.containterNowPlaying,
                                                   manager=self.manager, 
                                                   object_id=ObjectID(class_id='@now_playing_labels'))
        self.lblTrackArtist = UILabel(relative_rect=pygame.Rect((177,25 ), (120, 21)),
                                                     text = self.CurrentArtist, 
                                                     container = self.containterNowPlaying,
                                                     manager=self.manager, 
                                                     object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.lblTrackAlbum = UILabel(relative_rect=pygame.Rect((177,45 ), (120, 21)),
                                                       text = self.CurrentAlbum,
                                                       container = self.containterNowPlaying,
                                                       manager=self.manager, 
                                                       object_id=ObjectID(class_id='@now_playing_labels'))
                        
        self.lblTrackGenre = UILabel(relative_rect=pygame.Rect((177,65 ), (120, 21)),
                                                      text = self.CurrentGenre,
                                                      container = self.containterNowPlaying,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.lblTrackPlaylist = UILabel(relative_rect=pygame.Rect((210, 120 ), (41, 41)),
                                                        text = 'Play', 
                                                        container = self.containterNowPlaying,
                                                        manager=self.manager, 
                                                        object_id=ObjectID(class_id='@now_playing_labels'))
                                                                                          
        self.imgAlbumArt = UIImage(relative_rect=pygame.Rect((10, 0 ), (128, 128)),
                                                       image_surface=self.CurrentAlbumArt, 
                                                       container = self.containterNowPlaying,
                                                       manager=self.manager)
                                                       
        self.bPlay = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                                      text='Audiobooks',
                                                      container = self.containterMainWindow,
                                                      manager=self.manager, 
                                                      object_id=ObjectID(class_id='@now_playing_buttons', 
                                                                                      object_id='#play_button'))
                                                                                          
        self.pbarCurrentPosition = UIProgressBar(relative_rect=pygame.Rect((58, 180), (210, 15)),
                                                                          container = self.containterNowPlaying,
                                                                          manager=self.manager)
                                                                                                       
        self.lblCurrentPosition = UILabel(relative_rect=pygame.Rect((2, 178), (56, 20)),
                                                            text='00:00:00',
                                                            container = self.containterNowPlaying,
                                                            manager=self.manager, 
                                                            object_id=ObjectID(class_id='@now_playing_labels'))
        
        self.lblTrackDuration = UILabel(relative_rect=pygame.Rect((263, 178), (56, 20)),
                                                            text=self.CurrentDurationFormat,
                                                            container = self.containterNowPlaying,
                                                            manager=self.manager, 
                                                            object_id=ObjectID(class_id='@now_playing_labels'))
   
        self.containterNowPlaying.add_element(self.imgAlbumArt)
        self.containterNowPlaying.add_element(self.lblTrackTitle)
        self.containterNowPlaying.add_element(self.lblTrackArtist)
        self.containterNowPlaying.add_element(self.lblTrackAlbum)
        self.containterNowPlaying.add_element(self.lblTrackGenre)
        self.containterNowPlaying.add_element(self.lblTrackPlaylist)
        self.containterNowPlaying.add_element(self.pbarCurrentPosition) 
        self.containterNowPlaying.add_element(self.lblCurrentPosition)
        
        return self.containterNowPlaying, self.piPodAudio
    
    def HideNowPlayingScreen(self):
        self.containterNowPlaying.hide()
        # btnAlbumArt.hide()

    def ShowNowPlayingScreen(self, SelectedPlaylistId, SelectedTrackId):
        self.SelectedPlaylistId = SelectedPlaylistId
        self.SelectedTrackId = SelectedTrackId
        dfTrack = self.musicDB.getTrackFromDB(self.SelectedTrackId)
        sCurrentTrackFile = os.path.join(dfTrack['FileLocation'].iloc[0],  dfTrack['FileName'].iloc[0])
        currentTrack = self.piPodAudio.setTrack(sCurrentTrackFile)
        currentPlaylist = self.musicDB.getPlaylistInfoFromDB(SelectedPlaylistId)
        currentArtwork = currentTrack['artwork'] 
        bytesCurrentImage = currentArtwork.first.data
        pilCurrentImage = Image.open(BytesIO(bytesCurrentImage))
        
        pilCurrentImage = pilCurrentImage.resize((150, 150), 0)
        self.CurrentAlbumArt =  pygame.image.frombytes(pilCurrentImage.tobytes('raw'), (150, 150), 'RGB')
        self.CurrentTitle = str(currentTrack['title'])
        self.CurrentArtist = str(currentTrack['artist'])
        self.CurrentAlbum = str(currentTrack['album'])
        self.CurrentGenre = str(currentTrack['genre'])
        self.CurrentPlaylist = currentPlaylist.loc[0]['Playlist']
        self.CurrentDurationSeconds = round(float(str(currentTrack['#length'])))
        self.CurrentDurationFormat = str(datetime.timedelta(seconds=self.CurrentDurationSeconds))
        
        
        self.musicDB.setNowPlayingPlaylist(self.SelectedPlaylistId ,  self.SelectedTrackId)
        self.musicDB.setNowPlayingTrack( self.SelectedTrackId,  self.CurrentDurationSeconds,  0, 0)
        self.containterNowPlaying.kill()
        pygame.display.flip()
        self.containterNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(self.background.get_rect()), manager=self.manager, visible = 1)
        self.NowPlayingScreen()
        
    def MusicScreen(self):
        self.bPlaylists = UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                            text='Playlists',
                                            container = self.containterMusic,
                                            manager=self.manager)
        
        self.bAlbums = UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                                text='Albums',
                                                container = self.containterMusic,
                                            manager=self.manager)
        self.bArtists = UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                              text='Artists',
                                              container = self.containterMusic,
                                              manager=self.manager) 
                                            
        self.bGenres = UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                               text='Genres',
                                               container = self.containterMusic,
                                               manager=self.manager)
        
        self.containterMusic.add_element(self.bPlaylists)
        self.containterMusic.add_element(self.bAlbums)
        self.containterMusic.add_element(self.bArtists)
        self.containterMusic.add_element(self.bGenres)
        return self.containterMusic
    
    def HideMusicScreen(self):
         self.containterMusic.hide()
        # btnAlbumArt.hide()


    def ShowMusicScreen(self):
         self.containterMusic.show()
        
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
