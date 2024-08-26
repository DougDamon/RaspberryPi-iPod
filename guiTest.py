import os
import pygame
import pygame_gui
from common.pipodconfiguration import piPodConfiguration
import common.pipodgui as piPodGUI
from common.musicdatabase import MusicDB

configuration = piPodConfiguration()
themeFile =os.path.join(configuration.ThemeDirectory,  configuration.ThemeFile)
musicDB = MusicDB()
piPodAudioControls = None 
pygame.init()
pygame.display.set_caption('piPod')
window_surface = pygame.display.set_mode((320,240))
background = pygame.Surface((320,240))
background.fill(pygame.Color('aquamarine1'))
#'#000001'))
manager = pygame_gui.UIManager((320,240), themeFile)
#containterMainWindow = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager)
#containterNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager, visible = 0)
#containterMusic = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager, visible = 0)

clock = pygame.time.Clock()
is_running = True

piPod = piPodGUI.piPodGUI(clock,  window_surface,  background, manager)


MainScreenContainer = piPod.MainScreen()

MusicContainer = piPod.MusicScreen()
AvailablePlaylistContainer = piPod.AvailablePlaylistsScreen()
SelectedPlaylistContainer = piPod.PlaylistTracksScreen()


SelectedNowPlayingPlaylistId = None
SelectedNowPlayingTrackId = None



while is_running:
    time_delta = clock.tick(60)/1000.0
#    print('selectlist:',  pygame_gui.UI_SELECTION_LIST_NEW_SELECTION)
    for event in pygame.event.get():
        manager.process_events(event)
        match event.type:
            case pygame.QUIT:
                is_running = False
            case pygame_gui.UI_BUTTON_PRESSED:
                match event.ui_element:
                    case piPod.bNowPlaying:
                        piPod.HideMainScreen()
                        window_surface.blit(background, (0, 0))
                        piPod.ShowNowPlayingScreen()
                        piPod.containterMainWindow.hide()
                        pygame.display.flip()
                    case piPod.bMusic:
                        piPod.HideMainScreen()
                        window_surface.blit(background, (0, 0))
                        piPod.ShowMusicScreen()
                        pygame.display.flip()
                    case piPod.bPlaylists:
                        piPod.HideMusicScreen()
                        piPod.ShowAvailablePlaylistsScreen()
                        pygame.display.flip()  
                    case _:
                        pass
            case pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                match event.ui_element:
                    case piPod.sPlaylistSelectionList:
                        piPod.HideAvailablePlaylistsScreen()
                        selectedPlaylist = piPod.sPlaylistSelectionList.get_single_selection()
                        SelectedNowPlayingPlaylistId = musicDB.getPlaylistIdbyNamefromDB(selectedPlaylist)
                        piPod.ShowPlaylistTracksScreen(SelectedNowPlayingPlaylistId)                 
                    case piPod.sPlaylistTracks:
                        piPod.HidePlaylistTracksScreen()
                        selectedTrack = piPod.sPlaylistTracks.get_single_selection()
                        SelectedNowPlayingTrackId = str(musicDB.getTrackIdByNameFromDB(SelectedNowPlayingPlaylistId,  selectedTrack))
                        NowPlayingContainer,  piPodAudioControls = piPod.NowPlayingScreen() #SelectedNowPlayingPlaylistId,  SelectedNowPlayingTrackId)
                        piPod.HidePlaylistTracksScreen()
#                        window_surface.blit(background, (0, 0))
#                        pygame.display.update()
                        window_surface.blit(background, (0, 0))
                        piPod.ShowNowPlayingScreen(SelectedNowPlayingPlaylistId,  SelectedNowPlayingTrackId)
                        pygame.display.flip()
                    case _:
                        pass
#                        print('other')
            case _:
                pass
    manager.process_events(event)
    manager.update(time_delta)
    # window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()
pygame.quit()
