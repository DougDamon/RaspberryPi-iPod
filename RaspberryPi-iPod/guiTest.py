#import os
#import datetime
#import pygame
#import pygame_gui
from common.pipodconfiguration import piPodConfiguration
import common.pipodgui as piPodGUI
from common.musicdatabase import MusicDB

configuration = piPodConfiguration()
#themeFile =os.path.join(configuration.ThemeDirectory,  configuration.ThemeFile)
musicDB = MusicDB()
#piPodAudio = AudioPlayback()
#piPodAudioControls = None 
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
currentPosition = 0



#PlayContainer = piPod.Play()
#PlayContainer.hide()
#piPod.Pause()
#PauseContainer.hide()


#SelectedNowPlayingPlaylistId = None
#SelectedNowPlayingTrackId = None
CurrentPlaylistId = None
CurrentTrackId = None
#NextPlaylistId = None
NextTrackSet = False

#piPodGUI.ShowMainScreen()

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in piPodGUI.getEvent():
        piPodGUI.manager.process_events(event)
        match event.type:
            case piPodGUI.QUIT:
                is_running = False
            case piPodGUI.UI_BUTTON_PRESSED:
                match event.ui_element:
                    case piPodGUI.bNowPlaying:
                        piPodGUI.HideMainScreen()
                        piPodGUI.ShowNowPlayingScreen()
                    case piPodGUI.bMusic:
                        piPodGUI.HideMainScreen()
                        piPodGUI.ShowMusicScreen()
                    case piPodGUI.bPlaylists:
                        piPodGUI.HideMusicScreen()
                        piPodGUI.ShowAvailablePlaylistsScreen()
                    case piPodGUI.bPlay:
                        piPodGUI.Play()
#                        piPodGUI.Pause()
#                        piPodGUI.display.flip()
#                        piPodAudio.playTrack()
                        isMusicPlaying = True
                        isMusicPaused = False
                    case piPodGUI.bPause:
                        piPodGUI.Pause()
#                        piPodGUI.display.flip()
#                        piPodGUI.piPodAudio.pauseTrack()
                        NextTrack = None
                        isMusicPaused = True                    
                    case piPodGUI.bForward:
                        piPodGUI.NextTrackNowPlaying()
                    case piPodGUI.bRewind:
                        isMusicPlaying = False
                        piPodGUI.PreviousTrackNowPlaying()
                        isMusicPlaying = True
                    case _:
                        pass
            case piPodGUI.UI_SELECTION_LIST_NEW_SELECTION:
                match event.ui_element:
                    case piPodGUI.sPlaylistSelectionList:
                        piPodGUI.HideAvailablePlaylistsScreen()
                        selectedPlaylist = piPodGUI.sPlaylistSelectionList.get_single_selection()
                        SelectedNowPlayingPlaylistId = musicDB.getPlaylistIdbyNamefromDB(selectedPlaylist)
                        piPodGUI.setCurrentPlaylist(SelectedNowPlayingPlaylistId)
                        piPodGUI.ShowPlaylistTracksScreen()                 
                    case piPodGUI.sPlaylistTracks:
                        piPodGUI.HidePlaylistTracksScreen()
                        selectedTrack = piPodGUI.sPlaylistTracks.get_single_selection()
                        SelectedNowPlayingTrackId = str(musicDB.getTrackIdByNameFromDB(SelectedNowPlayingPlaylistId,  selectedTrack))
#                        NowPlayingContainer,  piPodAudioControls = piPod.NowPlayingScreen() #SelectedNowPlayingPlaylistId,  SelectedNowPlayingTrackId)
                        piPodGUI.HidePlaylistTracksScreen()
                        piPodGUI.setCurrentTrack(SelectedNowPlayingTrackId)
                        piPodGUI.ShowNowPlayingScreen()
                    case _:
                        pass
#                        print('other')
            case piPodGUI.MUSIC_END:
                piPodGUI.NextTrackNowPlaying()
#                print('MusicEndEvent',  piPodGUI.MUSICENDEVENT)
            case _:
                pass
    if isMusicPlaying == True:
        piPodGUI.updateCurrentPosition()
        
#        if not NextTrackSet:
#            print('Setting Next Track')
#            piPodGUI.setNowPlayingNextTrack()
#            print()
            
#    piPodGUI.manager.process_events(event)
    piPodGUI.manager.update(time_delta)
    # window_surface.blit(background, (0, 0))
    piPodGUI.drawScreen()
    piPodGUI.updateDisplay()
piPodGUI.quit()
