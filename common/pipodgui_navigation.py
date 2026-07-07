from common.pipodgui import piPodGUI
from common.input.rotary import RotaryEncoder
   
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
        """
        Set the default selected element for the Main screen.

        Only one Main screen navigation item should be selected at a time.
        If there is no current playlist/track, Now Playing is disabled and
        Music is selected. Otherwise Now Playing is selected.
        """

        # Clear any old Main screen selection boxes first.
        self.bNowPlaying.unselect()
        self.bMusic.unselect()
        self.bOTR.unselect()
        self.bAudiobooks.unselect()
        self.bGames.unselect()
        self.bManagement.unselect()

        if self.CurrentPlaylistId == None or self.CurrentTrackId == None:
            self.bNowPlaying.disable()
            self.bMusic.select()
            self.CurrentScreenElement = 'Music'
        else:
            self.bNowPlaying.enable()
            self.bNowPlaying.select()
            self.CurrentScreenElement = 'NowPlaying'

        self.markDirty()
    
    def getMainScreenWidget(self, element_name):
        """
        Return the pygame_gui widget for a Main screen navigation element.

        This keeps Main screen element-to-widget mapping in one place.
        It does not decide whether an element should be visible, enabled,
        disabled, or selected by default.
        """

        widgets = {
            "NowPlaying": self.bNowPlaying,
            "Music": self.bMusic,
            "OTR": self.bOTR,
            "Audiobooks": self.bAudiobooks,
            "Games": self.bGames,
            "Settings": self.bManagement,
            "Management": self.bManagement,
        }

        return widgets.get(element_name)

    def getNowPlayingWidget(self, element_name):
        """
        Return the pygame_gui widget for a simple Now Playing screen element.

        Repeat and Shuffle are intentionally not handled here because they
        use state-specific widgets/icons.
        """

        widgets = {
            "Play/Pause": self.bPause if self.getAudioPlayingStatus() else self.bPlay,
            "Forward": self.bForward,
            "Rewind": self.bRewind,
            "Back": self.bBack,
            "Home": self.bHome,
        }

        return widgets.get(element_name)
 
    def getMusicScreenWidget(self, element_name):
        """
        Return the pygame_gui widget for a Music screen navigation element.

        This keeps Music screen element-to-widget mapping in one place.
        """

        widgets = {
            "AvailablePlaylists": self.bPlaylists,
            "Albums": self.bAlbums,
            "Artists": self.bArtists,
            "Genres": self.bGenres,
            "Back": self.bBack,
            "Home": self.bHome,
        }

        return widgets.get(element_name)

    def getCurrentListItemWidget(self):
        """
        Return the currently selected pygame_gui list item widget.

        AvailablePlaylists and PlaylistTracks are dynamic list screens. Their
        selectable elements are not fixed buttons. They are list items looked up
        by the current screen element index.
        """

        item_index = self.getCurrentScreenElementIndex()

        match self.CurrentScreen:
            case 'AvailablePlaylists':
                return self.sPlaylistSelectionList.item_list_container.elements[item_index]

            case 'PlaylistTracks':
                return self.sPlaylistTracks.item_list_container.elements[item_index]

            case _:
                return None
 
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
                widget = self.getMainScreenWidget(Element)

                if widget is not None:
                    widget.select()
                    
            case 'NowPlaying':
                match Element:
                    case 'Play/Pause' | 'Forward' | 'Rewind' | 'Back' | 'Home':
                        widget = self.getNowPlayingWidget(Element)

                        if widget is not None:
                            widget.select()
                            
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
                                self.bShuffleOff.select()
                            case 'On':
                                self.ShowShuffleButtonOff()
                                self.bShuffleOn.select()    
                    case _:
                        pass
                        
            case 'Music':
                widget = self.getMusicScreenWidget(Element)

                if widget is not None:
                    widget.select()
                    
            case 'AvailablePlaylists' | 'PlaylistTracks':
                widget = self.getCurrentListItemWidget()

                if widget is not None:
                    widget.change_object_id('@navigation_buttons')
                    widget.select()
                
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
        self.markDirty()

    def setScreenElementUnselected(self, Element):
        match self.CurrentScreen:
            case 'Main':
                widget = self.getMainScreenWidget(Element)

                if widget is not None:
                    widget.unselect()
                    
            case 'NowPlaying':
                match Element:
                    case 'Play/Pause' | 'Forward' | 'Rewind' | 'Back' | 'Home':
                        widget = self.getNowPlayingWidget(Element)

                        if widget is not None:
                            widget.unselect()
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
                        if self.Shuffle == 'Off':
                            self.bShuffleOn.unselect()
                        else:
                            self.bShuffleOn.select()
                    case _:
                        pass
                        
            case 'Music':
                widget = self.getMusicScreenWidget(Element)

                if widget is not None:
                    widget.unselect()
                    
            case 'AvailablePlaylists' | 'PlaylistTracks':
                widget = self.getCurrentListItemWidget()

                if widget is not None:
                    widget.unselect()
                    
            case 'OTR':
                pass
            case 'Audiobooks':
                pass
            case 'Games':
                pass
            case 'Settings':
                pass
        self.markDirty()
        
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
    
    def selectMainScreenElement(self):
        """
        Handle selection behavior for the Main screen.
        """

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
    
    def selectMusicScreenElement(self):
        """
        Handle selection behavior for the Music screen.
        """

        self.navigationPath.append('Music')

        match self.CurrentScreenElement:
            case 'AvailablePlaylists':
                print(f"self.CurrentPlaylistInfo: {self.CurrentPlaylistInfo},  {type(self.CurrentPlaylistInfo)}")

                if self.CurrentPlaylistInfo.shape[0] == 0:
                    playlistIndex = 0
                else:
                    playlistIndex = self.getScreenElementIndex(
                        'AvailablePlaylists',
                        self.CurrentPlaylistInfo.iloc[0]['Playlist']
                    )

                playlists = list(self.getAvailablePlaylists()['Playlist'])
                self.ScreenNavigation['AvailablePlaylists'] = playlists

                self.setCurrentScreenElement(
                    'AvailablePlaylists',
                    playlists[playlistIndex]
                )

                self.MusicScreenHide()
                self.AvailablePlaylistsScreenShow()
                self.setScreenElementSelected(
                    self.ScreenNavigation[self.CurrentScreen][self.getCurrentScreenElementIndex()]
                )

            case 'Albums':
                pass

            case 'Artists':
                pass

            case 'Genres':
                pass

            case _:
                pass
    
    def selectAvailablePlaylist(self):
        """
        Handle selection behavior for the Available Playlists screen.
        """

        self.navigationPath.append('AvailablePlaylists')

        selectedPlaylist = self.CurrentScreenElement
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
    
    def selectPlaylistTrack(self):
        """
        Handle selection behavior for the Playlist Tracks screen.
        """

        self.navigationPath.append('PlaylistTracks')

        selectedTrack = self.CurrentScreenElement

        self.setCurrentScreenElement('NowPlaying', 'Play/Pause')

        selectedTrackId = self.getTrackIdByNameFromDB(
            self.CurrentPlaylistId,
            selectedTrack
        )

        self.setSelectedTrack(selectedTrackId)

        self.PlaylistTracksScreenHide()
        self.NowPlayingScreenShow()
        self.setScreenElementSelected(self.CurrentScreenElement)
        
    def hideCurrentScreen(self):
        """
        Hide whichever screen is currently active.
    
        This keeps screen-hiding behavior in one place and reuses the existing
        generic hide(ScreenName) method from piPodGUI.
        """
    
        self.hide(self.CurrentScreen)
                
    def goHome(self):
        """
        Return to the Main screen from the current screen.

        This centralizes Home behavior so UI buttons and future hardware
        shortcuts can use the same path.
        """

        self.setScreenElementUnselected(self.CurrentScreenElement)
        self.hideCurrentScreen()

        self.setCurrentScreen('Main')
        self.MainScreenShow()
        self.setMainScreenElementDefault()

    def goBack(self):
        """
        Return to the previous screen using navigationPath.

        This centralizes Back behavior so the Now Playing Back button and
        future rotary Left button can use the same path.
        """

        print("Back from screen:", self.CurrentScreen)
        print("navigationPath before back:", self.navigationPath)

        if len(self.navigationPath) == 0:
            print("No previous screen. Staying on current screen.")
            return

        previous_screen = self.navigationPath.pop()

        self.setScreenElementUnselected(self.CurrentScreenElement)
        self.hideCurrentScreen()
        
        match previous_screen:
            case 'Main':
                self.setCurrentScreen('Main')
                self.MainScreenShow()
                self.setMainScreenElementDefault()

            case 'Music':
                self.setCurrentScreenElement('Music', 'AvailablePlaylists')
                self.MusicScreenShow()
                self.setScreenElementSelected(self.CurrentScreenElement)

            case 'AvailablePlaylists':
                playlists = list(self.getAvailablePlaylists()['Playlist'])
                self.ScreenNavigation['AvailablePlaylists'] = playlists

                if self.CurrentPlaylistInfo.shape[0] == 0:
                    playlist_index = 0
                else:
                    playlist_index = self.getScreenElementIndex(
                        'AvailablePlaylists',
                        self.CurrentPlaylistInfo.iloc[0]['Playlist']
                    )

                self.setCurrentScreenElement(
                    'AvailablePlaylists',
                    playlists[playlist_index]
                )

                self.AvailablePlaylistsScreenShow()
                self.setScreenElementSelected(self.CurrentScreenElement)

            case 'PlaylistTracks':
                tracks = list(self.getPlaylistTracks(self.CurrentPlaylistId)['Title'])
                self.ScreenNavigation['PlaylistTracks'] = tracks

                self.setCurrentScreenElement('PlaylistTracks', tracks[0])
                self.PlaylistTracksScreenShow()
                self.setScreenElementSelected(self.CurrentScreenElement)

            case _:
                print("Back target not implemented:", previous_screen)

        print("navigationPath after back:", self.navigationPath)
        
    def selectNowPlayingElement(self):
        """
        Handle selection behavior for the Now Playing screen.
        """

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
                self.goBack()

            case 'Home':
                self.goHome()

            case _:
                pass
    
    def Select(self):
        match self.CurrentScreen:
            case 'Main':
                self.selectMainScreenElement()
            case 'NowPlaying':
                self.selectNowPlayingElement()
            case 'Music':
                self.selectMusicScreenElement()
            case 'AvailablePlaylists':
                self.selectAvailablePlaylist()
            case 'PlaylistTracks':
                self.selectPlaylistTrack()
                        
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
                match controlAction:
                    case 'Release':
                        self.goBack()
                    case 'Press':
                        pass
            
            # Right means "forward/proceed" in menus.
            # On NowPlaying, treat Right as a media-control shortcut for next track.
            # This can be revisited later if the control model changes.
            case 'Right':
                match controlAction:
                    case 'Release':
                        if self.CurrentScreen == 'NowPlaying':
                            self.NextTrackNowPlaying()
                        else:
                            self.Select()
                    case 'Press':
                        pass
