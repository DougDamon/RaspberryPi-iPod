import sys
import pygame
import pygame_gui
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage
from pygame_gui.ui_manager import UIManager


def getImage(imagePath):
    image = pygame.image.load(imagePath)
    print(image.get_rect())
    # image = pygame.transform.scale(image, (150, 150))
    return image
    
def MainScreen(containerMainWindow):
    bNowPlaying = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 0), (300, 24)),
                                               text='Now Playing',
                                               container = containerMainWindow,
                                               manager = manager
                                               )
    
    bMusic = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
                                          text='Music',
                                          container = containerMainWindow,
                                          manager=manager)

    bOTR = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
                                        text='OTR',
                                        container = containerMainWindow,
                                        manager=manager)

    bAudiobooks = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
                                               text='Audiobooks',
                                               container = containerMainWindow,
                                               manager=manager)

    bGames = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 120), (300, 24)),
                                          text='Games',
                                          container = containerMainWindow,
                                          manager=manager)

    bManagement = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 150), (300, 24)),
                                               text='Mangement',
                                               container = containerMainWindow,
                                               manager=manager)

    containerMainWindow.add_element(bNowPlaying) 
    containerMainWindow.add_element(bMusic)
    containerMainWindow.add_element(bOTR)
    containerMainWindow.add_element(bAudiobooks)
    containerMainWindow.add_element(bGames)
    containerMainWindow.add_element(bManagement)
    
    return bNowPlaying, bMusic, bOTR, bAudiobooks, bGames, bManagement
    
def MainScreenHide():
    containerMainWindow.hide()
    # manager.draw_ui(window_surface)
    # pygame.display.update()
    # window_surface.blit(background, (0, 0))
    # bNowPlaying.hide()
    # bMusic.hide()
    # bOTR.hide()
    # bAudiobooks.hide()
    # bGames.hide()
    # bManagement.hide()
    # window_surface.blit(background, (0, 0))

def MainScreenShow():
    containerMainWindow.show()
    # bNowPlaying.show()
    # bMusic.show()
    # bOTR.show()
    # bAudiobooks.show()
    # bGames.show()
    # bManagement.show()

def NowPlaying(containerMainWindow):
    pbarCurrentPosition = pygame_gui.elements.UIProgressBar(relative_rect=pygame.Rect((48, 180), (220, 15)),
                                                            manager=manager)
    lblCurrentPosition = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 178), (56, 20)),
                                                           text='00:00:00',
                                                           manager=manager)
    
    # albumArt = getImage(r'C:\Users\ddamon\OneDrive - Callon Petroleum Company\Documents\Personal\piPod\ui\resources/Moondawn.png')
    # btnAlbumArt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 0), (150, 150)),                                                
    #                                            text = 'x', # images = {'normal_image':{'path' : r'C:\Users\ddamon\OneDrive - Callon Petroleum Company\Documents\Personal\piPod\ui\resources/Moondawn.png'}},
    #                                            manager=manager)

    # pbMusic = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 30), (300, 24)),
    #                                        text='Music',
    #                                        manager=manager)

    # pbOTR = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 60), (300, 24)),
    #                                      text='OTR',
    #                                      manager=manager)

    # pbAudiobooks = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 90), (300, 24)),
    #                                             text='Audiobooks',
    #                                             manager=manager)

    # pbGames = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 120), (300, 24)),
    #                                        text='Games',
    #                                        manager=manager)

    # pbManagement = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((12, 150), (300, 24)),
    #                                             text='Mangement',
    #                                             manager=manager)
   
    containerNowPlaying.add_element(pbarCurrentPosition) 
    containerNowPlaying.add_element(lblCurrentPosition)
    # containerMainWindow.add_element(bOTR)
    return containerMainWindow
    
def HideNowPlaying():
    containerNowPlaying.hide()
    # btnAlbumArt.hide()


def ShowNowPlaying():
    containerNowPlaying.show()
