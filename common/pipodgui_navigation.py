from common.pipodgui import piPodGUI
from common.rotaryencoder import RotaryEncoder
   
class piPodGUINavigation(RotaryEncoder, piPodGUI):
    def __init__(self):
#        super().__init__()
        RotaryEncoder.__init__(self)
        piPodGUI.__init__(self)

        self.CurrentScreen = self.configuration.DefaultScreen
        self.CurrentScreenElement = self.configuration.DefaultElement
        self.PreviousScreen = self.configuration.DefaultScreen
        self.PreviousScreenElement = self.configuration.DefaultElement
        self.setMainScreenElementDefault()
        
    def setMainScreenElementDefault(self):
        if self.CurrentPlaylistId == None or self.CurrentTrackId == None:
            self.bNowPlaying.disable()
            self.bMusic.select()
        else:
            self.bNowPlaying.select()
            
    def setPlaylistNavigation(self):
        playlists = list(self.getDownloadedPlaylists(self.CurrentPlaylistId)['Title'])
        print(f'playlists: {playlists}')
        self.ScreenNavigation['PlaylistTracks'] = playlists
        self.CurrentPlaylistIndex = self.getScreenElementIndex('AvailablePlaylists',  self.CurrentPlaylistInfo.iloc[0]['Playlist'])
        
    def setCurrentScreen(self,  ScreenName):
        # Check id Screen is a configured 
        if ScreenName in self.Screens:
            self.PreviousScreen = self.CurrentScreen
            self.CurrentScreen = ScreenName
        else:
            print('error setting currentScreen')
    
    def setCurrentScreenElement(self,  ScreenName,  ScreenElement):
#        print(f'self.ScreenNavigation: {self.ScreenNavigation}')
        if ScreenName in self.ScreenNavigation and ScreenElement in self.ScreenNavigation[ScreenName]:
            self.setCurrentScreen(ScreenName)
            self.PreviousScreenElement = self.CurrentScreenElement
            self.CurrentScreenElement = ScreenElement
        else:
            print('error setting currentScreenElement')
            
    def getScreenElementIndex(self,  Screen,  ScreenElement):
        print(f"self.ScreenNavigation: {self.ScreenNavigation}")
        try:
            indexCurrentElement = self.ScreenNavigation[Screen].index(ScreenElement)
            return indexCurrentElement
        except ValueError:
            return 0
        else:
            print("Your age is:")
        
        
    def getCurrentScreenElementIndex(self):
        indexCurrentElement = self.getScreenElementIndex(self.CurrentScreen,  self.CurrentScreenElement)
        return indexCurrentElement

    def setScreenElementSelected(self,  Element):
        match self.CurrentScreen:
            case 'Main':
                match Element:
                    case 'NowPlaying':
                        self.setMainScreenElementDefault()
                    case 'Music':
                        self.bMusic.select()
                    case 'OTR':
                        self.bOTR.select()
                    case 'Audiobooks':
                        self.bAudiobooks.select()
                    case 'Games':
                        self.bGames.select()
                    case 'Settings':
                        self.bManagement.select()
                    case _:
                        pass
            case 'NowPlaying':
                match Element:
                    case 'Play/Pause':
                        if self.getAudioPlayingStatus() == False:
                            self.bPlay.select()
                        else:
                            self.bPause.select()
                    case 'Forward':
                        self.bForward.select()
                    case 'Rewind':
                        self.bRewind.select()
                    case 'Back':
                        self.bBack.select()
                    case 'Home':
                        self.bHome.select()
                    case 'Repeat':
                        match self.Repeat:
                            case 'Off':
                                self.ShowRepeatButtonOff()
                                self.bRepeatOff.select()
                            case 'On':
                                self.ShowRepeatButtonOn()
                                self.bRepeatOn.select()
                            case 'One':
                                self.ShowRepeatButtonOne()
                                self.bRepeatOne.select()
                    case 'Shuffle':
                        match self.Shuffle:
                            case 'Off':
                                self.ShowShuffleButtonOn()
                                self.bShuffleOn.select()
                            case 'On':
                                self.ShowShuffleButtonOff()
                                self.bShuffleOff.select()    
                    case _:
                        pass
            case 'Music':
                match Element:
                    case 'AvailablePlaylists':
                        self.bPlaylists.select()
                    case 'Albums':
                        self.bAlbums.select()
                    case 'Artists':
                        self.bArtists.select()
                    case 'Genres':
                        self.bGenres.select()
                    case 'Back':
                        self.bBack.select()
                    case 'Home':
                        self.bHome.select()
                    case _:
                        pass
            case'AvailablePlaylists':
                itemIndex = self.getCurrentScreenElementIndex()
                self.sPlaylistSelectionList.item_list_container.elements[itemIndex].change_object_id('@navigation_buttons')
                self.sPlaylistSelectionList.item_list_container.elements[itemIndex].select()                
            case'PlaylistTracks':
                itemIndex=self.getCurrentScreenElementIndex()
                print(f'itemIndex: {itemIndex}')
                self.sPlaylistTracks.item_list_container.elements[itemIndex].change_object_id('@navigation_buttons')
                self.sPlaylistTracks.item_list_container.elements[itemIndex].select()
            case 'OTR':
                pass
            case 'Audiobooks':
                pass
            case 'Games':
                pass
            case 'Settings':
                pass
        self.CurrentScreenElement = Element
        print(f'NewScreenElement: {self.CurrentScreenElement}')

    def setScreenElementUnselected(self, Element):
        match self.CurrentScreen:
            case 'Main':
                match Element:
                    case 'NowPlaying':
                        self.bNowPlaying.unselect()
                    case 'Music':
                        self.bMusic.unselect()
                    case 'OTR':
                        self.bOTR.unselect()
                    case 'Audiobooks':
                        self.bAudiobooks.unselect()
                    case 'Games':
                        self.bGames.unselect()
                    case 'Settings':
                        self.bManagement.unselect()
                    case _:
                        pass
            case 'NowPlaying':
                match Element:
                    case 'Play/Pause':
                        if self.getAudioPlayingStatus() == False:
                            self.bPlay.unselect()
                        else:
                            self.bPause.unselect()
                    case 'Forward':
                        self.bForward.unselect()
                    case 'Rewind':
                        self.bRewind.unselect()
                    case 'Back':
                        self.bBack.unselect()
                    case 'Home':
                        self.bHome.unselect()
                    case 'Repeat':
                        match self.Repeat:
                            case 'Off':
                                self.ShowRepeatButtonOff()
                                self.bRepeatOff.unselect()
                            case 'On':
                                self.ShowRepeatButtonOn()
                                self.bRepeatOn.unselect()
                            case 'One':
                                self.ShowRepeatButtonOne()
                                self.bRepeatOne.unselect()
                    case 'Shuffle':
                        match self.Shuffle:
                            case 'Off':
                                self.ShowShuffleButtonOff()
                                self.bShuffleOff.unselect()
                            case 'On':
                                self.ShowShuffleButtonOn()
                                self.bShuffleOn.unselect()
                    case _:
                        pass
                        
            case 'Music':
               match Element:
                    case 'AvailablePlaylists':
                        self.bPlaylists.unselect()
                    case 'Albums':
                        self.bAlbums.unselect()
                    case 'Artists':
                        self.bArtists.unselect()
                    case 'Genres':
                        self.bGenres.unselect()
                    case _:
                        pass
            case'AvailablePlaylists':
                itemIndex = self.getCurrentScreenElementIndex()
                self.sPlaylistSelectionList.item_list_container.elements[itemIndex].unselect()
            case'PlaylistTracks':
                itemIndex = self.getCurrentScreenElementIndex()
                self.sPlaylistTracks.item_list_container.elements[itemIndex].unselect()
            case 'OTR':
                pass
            case 'Audiobooks':
                pass
            case 'Games':
                pass
            case 'Settings':
                pass
    def NavigateUp(self, IndexCurrentElement):
#        lengthScreenNavigation = len(self.ScreenNavigation[self.CurrentScreen]) - 1
        if IndexCurrentElement  > 0:
            IndexCurrentElement = self.getCurrentScreenElementIndex()-1
            self.setScreenElementUnselected(self.CurrentScreenElement)
            self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
            self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])   
            print(f'indexCurrentElement: {IndexCurrentElement}')
        else:
            pass

    def NavigateDown(self, IndexCurrentElement):
        lengthScreenNavigation = len(self.ScreenNavigation[self.CurrentScreen]) - 1
        
        if IndexCurrentElement  < lengthScreenNavigation:
            IndexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)+1
            self.setScreenElementUnselected(self.CurrentScreenElement)
            self.CurrentScreenElement = self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement]
            self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][IndexCurrentElement])
            print(f'indexCurrentElement: {IndexCurrentElement}')
        else:
            pass
    def Select(self):
        match self.CurrentScreen:
            case 'Main':
                self.navigationPath.append('Main')
                match self.CurrentScreenElement:
                    case 'NowPlaying':                       
                        self.setCurrentScreenElement('NowPlaying', 'Play/Pause')
                        self.MainScreenHide()
                        self.NowPlayingScreenShow()
                        self.setScreenElementSelected(self.CurrentScreenElement)
                    case 'Music':
                        self.setCurrentScreenElement('Music', 'AvailablePlaylists')
                        self.MainScreenHide()
                        self.MusicScreen()
                        self.MusicScreenShow()
                        self.bPlaylists.select()
                    case 'OTR':
                        pass
                    case 'Audiobooks':
                        pass
                    case 'Games':
                        pass
                    case 'Settings':
                        pass
#            case 'NowPlaying':
#                pass
            case 'Music':
                self.navigationPath.append('Music')
                match self.CurrentScreenElement:
                    case 'AvailablePlaylists':
                        print(f"self.CurrentPlaylistInfo: {self.CurrentPlaylistInfo},  {type(self.CurrentPlaylistInfo)}")
                        if self.CurrentPlaylistInfo.shape[0] == 0:
                            playlistIndex = 0
                        else:
                            playlistIndex = self.getScreenElementIndex('AvailablePlaylists',  self.CurrentPlaylistInfo.iloc[0]['Playlist'])
                             
                        playlists = list(self.getAvailablePlaylists()['Playlist'])
                        self.ScreenNavigation['AvailablePlaylists'] = playlists
                        self.setCurrentScreenElement('AvailablePlaylists', playlists[playlistIndex])
                        self.MusicScreenHide()
                        self.AvailablePlaylistsScreenShow()
                        self.setScreenElementSelected(self.ScreenNavigation[self.CurrentScreen][self.getCurrentScreenElementIndex()])
                    case 'Music':
                        self.setCurrentScreenElement('Music', 'AvailablePlaylists')
                        self.MainScreenHide()
                        self.MusicScreenShow()
                        self.bPlaylists.select()
            case 'AvailablePlaylists':
                self.navigationPath.append('AvailablePlaylists')
                selectedPlaylist = self.CurrentScreenElement  #get the selected playlist
                trackIndex = 0
                self.setCurrentScreen('PlaylistTracks')
                selectedPlaylistId = self.musicDB.getPlaylistIdbyNamefromDB(selectedPlaylist)
                self.setCurrentPlaylist(selectedPlaylistId)
                tracks = list(self.getPlaylistTracks(self.CurrentPlaylistId)['Title'])
                print(f'tracks: {tracks}')
                self.ScreenNavigation['PlaylistTracks'] = tracks
                self.setCurrentScreenElement('PlaylistTracks', tracks[trackIndex])
                print(f'self.CurrentScreenElement: {self.CurrentScreenElement}')
                self.AvailablePlaylistsScreenHide()
                self.PlaylistTracksScreenShow()
                self.setScreenElementSelected(self.CurrentScreenElement)
            case 'PlaylistTracks':
                self.navigationPath.append('PlaylistTracks')
                selectedTrack = self.CurrentScreenElement  #get the selected track
#                self.setCurrentScreen('NowPlaying')
                self.setCurrentScreenElement('NowPlaying',  'Play/Pause') #self.ScreenNavigation[self.CurrentScreen][0])
                selectedTrackId = self.getTrackIdByNameFromDB(self.CurrentPlaylistId,  selectedTrack)
                self.setSelectedTrack(selectedTrackId)
                self.PlaylistTracksScreenHide()
                self.NowPlayingScreenShow()
                self.setScreenElementSelected(self.CurrentScreenElement)
            case 'NowPlaying':
#                Play/Pause, Forward, Rewind, Back, Home
                match self.CurrentScreenElement:
                    case 'Play/Pause':
                        if self.AudioPlaying == True:
                            self.Pause()
                        else:
                            self.Play()
                    case 'Forward':
                        self.NextTrackNowPlaying()
                    case 'Rewind':
                        self.PreviousTrackNowPlaying()
                    case 'Repeat':
                        match self.Repeat:
                            case 'Off':
                                self.RepeatOn()
                            case 'On':
                                self.RepeatOne()
                            case 'One':
                                self.RepeatOff()
                    case 'Shuffle':
                        match self.Shuffle:
                            case 'Off':
                                self.ShuffleOn()
                            case 'On':
                                self.ShuffleOff()
                    case 'Back':
                        match self.navigationPath.pop():
                            case 'PlaylistTracks':
                                tracks = list(self.getPlaylistTracks(self.CurrentPlaylistId)['Title'])
                                self.ScreenNavigation['PlaylistTracks'] = tracks
                                self.setCurrentScreenElement('PlaylistTracks', tracks[trackIndex])
                                self.NowPlayingScreenHide()
                                self.PlaylistTracksScreenShow()
                                self.setScreenElementSelected(self.CurrentScreenElement)
                                
                    case 'Home':
                        self.NowPlayingScreenHide()
                        self.MainScreenShow()
                        
    def EncoderNavigation(self, EncoderActivity):
#        print(f'EncoderActivity: {EncoderActivity}')
#        print(f'CurrentScreenElement: {self.CurrentScreenElement}')
        control = next(iter(EncoderActivity))
        controlAction = EncoderActivity[control]
        indexCurrentElement = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)
#        print(f'indexCurrentElement: {indexCurrentElement}') 
        
#        print(f'lengthScreenNavigation: {lengthScreenNavigation}')
        match control:
            case 'Wheel':
                match controlAction:
                    case 'Up':
                        self.NavigateUp(indexCurrentElement)
                    case 'Down':
                        self.NavigateDown(indexCurrentElement)
            case 'Select':
                match controlAction:
                    case 'Release':
                        self.Select()
                    case 'Press':
                        pass
            case 'Up':
                match controlAction:
                    case 'Release':
                        self.NavigateUp(indexCurrentElement)
                    case 'Press':
                        pass
                
            case 'Down':
                match controlAction:
                    case 'Release':
                        self.NavigateDown(indexCurrentElement)
                    case 'Press':
                        pass
                
            case 'Left':
                pass
                
            case 'Right':
                pass
