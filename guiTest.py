import os
import datetime
#import pygame
#import pygame_gui
from common.pipodconfiguration import piPodConfiguration
import common.pipodgui as piPodGUI
from common.musicdatabase import MusicDB
from common.pipodaudio import AudioPlayback

configuration = piPodConfiguration()
#themeFile =os.path.join(configuration.ThemeDirectory,  configuration.ThemeFile)
musicDB = MusicDB()
piPodAudio = AudioPlayback()
piPodAudioControls = None 
#pygame.init()
#pygame.display.set_caption('piPod')
#window_surface = pygame.display.set_mode((320,240))
#background = pygame.Surface((320,240))
#background.fill(pygame.Color('aquamarine1'))
#'#000001'))
#print(themeFile)
#manager = pygame_gui.UIManager((320,240),  themeFile)
#containerMainWindow = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager)
#containerNowPlaying = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager, visible = 0)
#containerMusic = pygame_gui.core.UIContainer(pygame.Rect(background.get_rect()), manager=manager, visible = 0)


is_running = True

piPodGUI = piPodGUI.piPodGUI()
clock = piPodGUI.getClock()


#MainScreenContainer = piPod.MainScreen()

#MusicContainer = piPod.MusicScreen()
#AvailablePlaylistContainer = piPod.AvailablePlaylistsScreen()
#SelectedPlaylistContainer = piPod.PlaylistTracksScreen()
#NowPlayingContainer,  ContainerPlay,  ContainerPause = piPod.NowPlayingScreen()

# Music
isMusicPlaying = False
isMusicPaused = False


#PlayContainer = piPod.Play()
#PlayContainer.hide()
#piPod.Pause()
#PauseContainer.hide()


SelectedNowPlayingPlaylistId = None
SelectedNowPlayingTrackId = None
NextTrack = None

#piPodGUI.ShowMainScreen()

while is_running:
    time_delta = clock.tick(10)/1000.0
    for event in piPodGUI.getEvent():
        piPodGUI.manager.process_events(event)
        match event.type:
            case piPodGUI.QUIT:
                is_running = False
            case piPodGUI.UI_BUTTON_PRESSED:
                match event.ui_element:
                    case piPodGUI.bNowPlaying:
                        piPodGUI.HideMainScreen()
#                        window_surface.blit(background, (0, 0))
                        piPodGUI.ShowNowPlayingScreen()
                        piPodGUI.HideMainScreen()
#                        piPodGUI.display.flip()
                    case piPodGUI.bMusic:
                        piPodGUI.HideMainScreen()
#                        window_surface.blit(background, (0, 0))
                        piPodGUI.ShowMusicScreen()
#                        piPodGUI.display.flip()
                    case piPodGUI.bPlaylists:
                        piPodGUI.HideMusicScreen()
                        piPodGUI.ShowAvailablePlaylistsScreen()
#                        piPodGUI.display.flip()
                    case piPodGUI.bPlay:
                        piPodGUI.Pause()
#                        piPodGUI.display.flip()
                        piPodAudio.playTrack()
                        isMusicPlaying = True
                        isMusicPaused = False
                    case piPodGUI.bPause:
                        piPodGUI.Play()
#                        piPodGUI.display.flip()
                        piPodGUI.piPodAudio.pauseTrack()
                        isMusicPaused = True
                    
                    case _:
                        pass
            case piPodGUI.UI_SELECTION_LIST_NEW_SELECTION:
                match event.ui_element:
                    case piPodGUI.sPlaylistSelectionList:
                        piPodGUI.HideAvailablePlaylistsScreen()
                        selectedPlaylist = piPodGUI.sPlaylistSelectionList.get_single_selection()
                        SelectedNowPlayingPlaylistId = musicDB.getPlaylistIdbyNamefromDB(selectedPlaylist)
                        piPodGUI.ShowPlaylistTracksScreen(SelectedNowPlayingPlaylistId)                 
                    case piPodGUI.sPlaylistTracks:
                        piPodGUI.HidePlaylistTracksScreen()
                        selectedTrack = piPodGUI.sPlaylistTracks.get_single_selection()
                        SelectedNowPlayingTrackId = str(musicDB.getTrackIdByNameFromDB(SelectedNowPlayingPlaylistId,  selectedTrack))
#                        NowPlayingContainer,  piPodAudioControls = piPod.NowPlayingScreen() #SelectedNowPlayingPlaylistId,  SelectedNowPlayingTrackId)
                        piPodGUI.HidePlaylistTracksScreen()
                        piPodGUI.piPodAudio.setTrack(SelectedNowPlayingTrackId)
                        piPodGUI.ShowNowPlayingScreen(SelectedNowPlayingPlaylistId,  SelectedNowPlayingTrackId)
                    case _:
                        pass
#                        print('other')
            case piPodAudio.MUSICENDEVENT:
                print('MusicEndEvent',  piPodAudio.MUSICENDEVENT)
            case _:
                pass
    if isMusicPlaying == True and isMusicPaused == False:
        currentPosition = piPodGUI.getCurrentPosition()
        print(currentPosition)
        currentDuration = piPodGUI.getCurrentDuration()
#        piPod.lblCurrentPosition.set_text = str(datetime.timedelta(seconds=currentPosition))
        piPodGUI.updateCurrentPosition(currentPosition,  time_delta)
#        if currentDuration - currentPosition < 5:
#            print('Setting Next Track')
#            NextTrack = musicDB.getNowPlayingNextTrack()
            
    piPodGUI.manager.process_events(event)
    piPodGUI.manager.update(time_delta)
    # window_surface.blit(background, (0, 0))
    piPodGUI.drawScreen()
    piPodGUI.updateDisplay()
piPodGUI.quit()
