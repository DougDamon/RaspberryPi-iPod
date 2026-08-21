from gpiozero import Button
from common.config.settings import ConfigService
import common.pipodgui_navigation as piPodGUI

from common.library.music_database import MusicDB

configuration = ConfigService()

musicDB = MusicDB()

# Side volume buttons.
# Each button connects its GPIO pin to ground when pressed.
volumeUpButton = Button(20, pull_up=True, bounce_time=0.05)
volumeDownButton = Button(26, pull_up=True, bounce_time=0.05)

# PiTFT display buttons.
displayButton1 = Button(16, pull_up=True, bounce_time=0.05)
displayButton2 = Button(22, pull_up=True, bounce_time=0.05)
displayButton3 = Button(23, pull_up=True, bounce_time=0.05)
displayButton4 = Button(27, pull_up=True, bounce_time=0.05)

volumeUpWasPressed = False
volumeDownWasPressed = False

displayButton1WasPressed = False
displayButton2WasPressed = False
displayButton3WasPressed = False
displayButton4WasPressed = False



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

    # Volume Up
    volumeUpIsPressed = volumeUpButton.is_pressed
    
    if volumeUpIsPressed and not volumeUpWasPressed:
        piPodGUI.VolumeUp()
    
    volumeUpWasPressed = volumeUpIsPressed
    
    
    # Volume Down
    volumeDownIsPressed = volumeDownButton.is_pressed
    
    if volumeDownIsPressed and not volumeDownWasPressed:
        print('vol down')
        piPodGUI.VolumeDown()
    
    volumeDownWasPressed = volumeDownIsPressed
    
    
    # PiTFT Button 1 - GPIO16
    displayButton1IsPressed = displayButton1.is_pressed
    
    if displayButton1IsPressed and not displayButton1WasPressed:
        print("Display Button 1 pressed - GPIO16")
    
    displayButton1WasPressed = displayButton1IsPressed
    
    
    # PiTFT Button 2 - GPIO22
    displayButton2IsPressed = displayButton2.is_pressed
    
    if displayButton2IsPressed and not displayButton2WasPressed:
        print("Display Button 2 pressed - GPIO22")
    
    displayButton2WasPressed = displayButton2IsPressed
    
    
    # PiTFT Button 3 - GPIO23
    displayButton3IsPressed = displayButton3.is_pressed
    
    if displayButton3IsPressed and not displayButton3WasPressed:
        print("Display Button 3 pressed - GPIO23")
    
    displayButton3WasPressed = displayButton3IsPressed
    
    
    # PiTFT Button 4 - GPIO27
    displayButton4IsPressed = displayButton4.is_pressed
    
    if displayButton4IsPressed and not displayButton4WasPressed:
        print("Display Button 4 pressed - GPIO27")
    
    displayButton4WasPressed = displayButton4IsPressed    
        
    for event in piPodGUI.getEvent():
        piPodGUI.manager.process_events(event)
#        print(f'Event: {event}')
        match event.type:
            case piPodGUI.QUIT:
                is_running = False
            case piPodGUI.UI_BUTTON_PRESSED:
                match event.ui_element:
                    case piPodGUI.bNowPlaying:
                            piPodGUI.setCurrentScreenElement(
                                "NowPlaying",
                                "Play/Pause"
                            )
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
    
    if piPodGUI.CurrentScreen == "NowPlaying":
    
        if piPodGUI.isDirty():
            piPodGUI.drawNowPlayingDirect()
    
        elif piPodGUI.isPositionDirty():
            piPodGUI.drawCurrentPosition()
    
    
    elif piPodGUI.CurrentScreen == "AvailablePlaylists":
    
        if piPodGUI.isDirty():
            piPodGUI.drawAvailablePlaylistsDirect()
    
    
    elif piPodGUI.CurrentScreen == "PlaylistTracks":
    
        if piPodGUI.isDirty():
            piPodGUI.drawPlaylistTracksDirect()
    
    
    else:
    
        if piPodGUI.isDirty():
            piPodGUI.drawScreen()
            piPodGUI.updateDisplay()
            piPodGUI.clearDirty()
            piPodGUI.clearPositionDirty()
     
volumeUpButton.close()
volumeDownButton.close()

displayButton1.close()
displayButton2.close()
displayButton3.close()
displayButton4.close()

piPodGUI.quit()
