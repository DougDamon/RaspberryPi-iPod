from common.pipodconfiguration import piPodConfiguration
import common.pipodgui_navigation as piPodGUI

from common.musicdatabase import MusicDB

configuration = piPodConfiguration()

musicDB = MusicDB()



is_running = True

piPodGUI = piPodGUI.piPodGUINavigation()
clock = piPodGUI.getClock()

# Music
isMusicPlaying = False
isMusicPaused = False
currentPosition = 0

CurrentPlaylistId = None
CurrentTrackId = None
NextTrackSet = False



# UI Navigation
#MainScreenUIElements = {'NowPlaying' : 1 ,  'Music' : 2,  'OTR' : 3, 'Audiobooks' : 4, 'Games' :  5,  'Management' : 6}
while is_running:
    time_delta = clock.tick(60)/1000.0
    encoderActivity = piPodGUI.getEncoderActivity()
    if encoderActivity != None:
        piPodGUI.EncoderNavigation(encoderActivity)

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
    if isMusicPlaying == True or piPodGUI.AudioPlaying == True:
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
