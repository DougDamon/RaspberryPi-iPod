#import sys
import pygame
import pygame_gui
#from pygame_gui.ui_manager import UIManager
#from pygame_gui.elements.ui_window import UIWindow
#from pygame_gui.elements.ui_image import UIImage
#from pygame_gui.ui_manager import UIManager

class piPodGUI():
    def __init__(self,  Background,  Manager):
        pygame.init()

        self.background = Background
        self.manager = Manager
        self.containterMainWindow = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager)
        self.containterNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager, visible = 0)
        self.containterMusic = pygame_gui.core.UIContainer(pygame.Rect(Background.get_rect()), manager=Manager, visible = 0)
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
    
    def MainScreen(self):        
        self.bNowPlaying = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                                text='Now Playing',
                                                container = self.containterMainWindow,
                                                manager = self.manager
                                                )
    
        self.bMusic = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                            text='Music',
                                            container = self.containterMainWindow,
                                            manager=self.manager)

        self.bOTR = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                            text='OTR',
                                            container = self.containterMainWindow,
                                            manager=self.manager)

        self.bAudiobooks = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                                text='Audiobooks',
                                                container = self.containterMainWindow,
                                                manager=self.manager)

        self.bGames = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 120), (300, 24)),
                                            text='Games',
                                            container = self.containterMainWindow,
                                            manager=self.manager)

        self.bManagement = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 150), (300, 24)),
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

    def NowPlaying(self):
        pbarCurrentPosition = pygame_gui.elements.UIProgressBar(relative_rect=pygame.Rect((48, 180), (220, 15)),
                                                                                                       container = self.containterNowPlaying,
                                                                                                       manager=self.manager)
        lblCurrentPosition = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 178), (56, 20)),
                                                                                          text='00:00:00',
                                                                                          container = self.containterNowPlaying,
                                                                                          manager=self.manager)
   
        self.containterNowPlaying.add_element(pbarCurrentPosition) 
        self.containterNowPlaying.add_element(lblCurrentPosition)
        return self.containterNowPlaying
    
    def HideNowPlaying(self):
        self.containterNowPlaying.hide()
        # btnAlbumArt.hide()


    def ShowNowPlaying(self):
        self.containterNowPlaying.show()
        
    def Music(self):
        bPlaylists = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                            text='Playlists',
                                            container = self.containterMusic,
                                            manager=self.manager)
        
        bAlbums = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                            text='Albums',
                                            container = self.containterMusic,
                                            manager=self.manager)
        bArtists = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                            text='Artists',
                                            container = self.containterMusic,
                                            manager=self.manager) 
                                            
        bGenres = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                            text='Genres',
                                            container = self.containterMusic,
                                            manager=self.manager)
        
        self.containterMusic.add_element(bPlaylists)
        self.containterMusic.add_element(bAlbums)
        self.containterMusic.add_element(bArtists)
        self.containterMusic.add_element(bGenres)
        return self.containterMusic
    
    def HideMusic(self,  Container):
        Container.hide()
        # btnAlbumArt.hide()


    def ShowMusic(self,  Container):
        Container.show()
