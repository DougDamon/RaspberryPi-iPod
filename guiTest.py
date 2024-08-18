#import sys
import pygame
import pygame_gui
#from pygame_gui.ui_manager import UIManager
#from pygame_gui.elements.ui_window import UIWindow
#from pygame_gui.elements.ui_image import UIImage
#from pygame_gui.ui_manager import UIManager

import common.pipodgui as piPodGUI

pygame.init()
pygame.display.set_caption('piPod')
window_surface = pygame.display.set_mode((320,240))
background = pygame.Surface((320,240))
background.fill(pygame.Color('#000001'))
manager = pygame_gui.UIManager((320,240))
#containterMainWindow = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager)
#containterNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager, visible = 0)
#containterMusic = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager, visible = 0)

piPod = piPodGUI.piPodGUI(background, manager)

MainScreenContainer = piPod.MainScreen()
print(piPod.containterMainWindow)
NowPlayingContainer = piPod.NowPlaying()
print(piPod.containterNowPlaying)
MusicContainer = piPod.Music()
print(piPod.containterMusic)
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                is_running = False
            case pygame_gui.UI_BUTTON_PRESSED:
                match event.ui_element:
                    case piPod.bNowPlaying:
                        # HideMainScreen()
                        # pygame.display.update()
                        piPod.HideMainScreen()
                        # containterMainWindow.remove_element(bManagement)
                        # pygame.display.flip()
                        window_surface.blit(background, (0, 0))
                        piPod.containterNowPlaying = piPod.NowPlaying()
                        piPod.ShowNowPlaying()
                        piPod.containterMainWindow.hide()
#                        imgAlbumArt = getImage(r'C:\_piPod\images/Moondawn_thumbnail.png')
#                        piPod.window_surface.blit(imgAlbumArt, imgAlbumArt.get_rect())
                        pygame.display.flip()
                        # ShowNowPlaying()
                    case piPod.bMusic:
                        piPod.HideMainScreen()
                        window_surface.blit(background, (0, 0))
                        piPod.ShowMusic(MusicContainer)
                        pygame.display.flip()
                    
    manager.process_events(event)
    manager.update(time_delta)
    # window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()
pygame.quit()
