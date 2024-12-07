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
#piPodGUI.bNowPlaying.select()
#currentUIElement = {'MainScreen':'NowPlaying'}


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

#piPodGUI.MainScreenShow()

# UI Navigation
#MainScreenUIElements = {'NowPlaying' : 1 ,  'Music' : 2,  'OTR' : 3, 'Audiobooks' : 4, 'Games' :  5,  'Management' : 6}
while is_running:
    time_delta = clock.tick(60)/1000.0
    encoderActivity = piPodGUI.rotaryEncoder.getEncoderActivity()
    if encoderActivity != None:
        piPodGUI.EncoderNavigation(encoderActivity)
#        control = next(iter(encoderActivity))
#        controlAction = encoderActivity[control]
#        currentScreen = next(iter(currentUIElement))
#        currentElement = currentUIElement[currentScreen]
#        match currentScreen:
#            case 'MainScreen':
#                match currentElement:
#                    case 'NowPlaying':
#                        match control:
#                            case 'Wheel':
#                                match controlAction:
#                                    case 'Up':
#                                        pass
#                                    case 'Down':
#                                        currentUIElement[currentScreen] = 'Music'
#                                        piPodGUI.bNowPlaying.unselect()
#                                        piPodGUI.bMusic.select()
#                            case _:
#                                pass
#                    case 'Music':
#                        match control:
#                            case 'Wheel':
#                                match controlAction:
#                                    case 'Up':
#                                        currentUIElement[currentScreen] = 'NowPlaying'
#                                        piPodGUI.bMusic.unselect()
#                                        piPodGUI.bNowPlaying.select()
#                                    case 'Down':
#                                        currentUIElement[currentScreen] = 'OTR'
#                                        piPodGUI.bMusic.unselect()
#                                        piPodGUI.bOTR.select()
#                            case _:
#                                pass
#                    case 'OTR': 
#                        match control:
#                            case 'Wheel':
#                                match controlAction:
#                                    case 'Up':
#                                        currentUIElement[currentScreen] = 'Music'
#                                        piPodGUI.bOTR.unselect()
#                                        piPodGUI.bMusic.select()
#                                    case 'Down':
#                                        currentUIElement[currentScreen] = 'Audiobooks'
#                                        piPodGUI.bOTR.unselect()
#                                        piPodGUI.bAudiobooks.select()
#                            case _:
#                                pass  
#                    case 'Audiobooks':
#                        match control:
#                            case 'Wheel':
#                                match controlAction:
#                                    case 'Up':
#                                        currentUIElement[currentScreen] = 'OTR'
#                                        piPodGUI.bAudiobooks.unselect()
#                                        piPodGUI.bOTR.select()
#                                    case 'Down':
#                                        currentUIElement[currentScreen] = 'Games'
#                                        piPodGUI.bAudiobooks.unselect()
#                                        piPodGUI.bGames.select()
#                            case _:
#                                pass
#                    case 'Games':  
#                        match control:
#                            case 'Wheel':
#                                match controlAction:
#                                    case 'Up':
#                                        currentUIElement[currentScreen] = 'Audiobooks'
#                                        piPodGUI.bGames.unselect()
#                                        piPodGUI.bAudiobooks.select()
#                                    case 'Down':
#                                        currentUIElement[currentScreen] = 'Management'
#                                        piPodGUI.bGames.unselect()
#                                        piPodGUI.bManagement.select()
#                            case _:
#                                pass
#                    case 'Management':
#                        match control:
#                            case 'Wheel':
#                                match controlAction:
#                                    case 'Up':
#                                        currentUIElement[currentScreen] = 'Games'
#                                        piPodGUI.bManagement.unselect()
#                                        piPodGUI.bGames.select()
#                                    case 'Down':
#                                        pass
#                            case _:
#                                pass
#                    case _:
#                        pass
#            case _:
#                pass
    for event in piPodGUI.getEvent():
        piPodGUI.manager.process_events(event)
#        print(f'Event: {event}')
        match event.type:
            case piPodGUI.QUIT:
                is_running = False
            case piPodGUI.UI_BUTTON_PRESSED:
                match event.ui_element:
                    case piPodGUI.bNowPlaying:
                        piPodGUI.MainScreenHide()
                        piPodGUI.NowPlayingScreenShow()
                    case piPodGUI.bMusic:
                        piPodGUI.MainScreenHide()
                        piPodGUI.MusicScreenShow()
                    case piPodGUI.bPlaylists:
                        piPodGUI.MusicScreenHide()
                        piPodGUI.AvailablePlaylistsScreenShow()
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
                    case piPodGUI.bHome:
                        print('home')
                        piPodGUI.NowPlayingScreenHide()
                        piPodGUI.MainScreenShow()
                    case _:
                        pass
            case piPodGUI.UI_SELECTION_LIST_NEW_SELECTION:
                match event.ui_element:
                    case piPodGUI.sPlaylistSelectionList:
                        piPodGUI.NowPlayingScreenShow()
                        selectedPlaylist = piPodGUI.sPlaylistSelectionList.get_single_selection()
                        SelectedNowPlayingPlaylistId = musicDB.getPlaylistIdbyNamefromDB(selectedPlaylist)
                        piPodGUI.setCurrentPlaylist(SelectedNowPlayingPlaylistId)
                        piPodGUI.PlaylistTracksScreenShow()                 
                    case piPodGUI.sPlaylistTracks:
                        piPodGUI.PlaylistTracksScreenHide()
                        selectedTrack = piPodGUI.sPlaylistTracks.get_single_selection()
                        SelectedNowPlayingTrackId = str(musicDB.getTrackIdByNameFromDB(SelectedNowPlayingPlaylistId,  selectedTrack))
#                        NowPlayingContainer,  piPodAudioControls = piPod.NowPlayingScreen() #SelectedNowPlayingPlaylistId,  SelectedNowPlayingTrackId)
                        piPodGUI.PlaylistTracksScreenHide()
                        piPodGUI.setCurrentTrack(SelectedNowPlayingTrackId)
                        piPodGUI.NowPlayingScreenShow()
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
