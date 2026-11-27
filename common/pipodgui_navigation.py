from common.pipodgui import piPodGUI
from common.input.rotary import RotaryEncoder
from common.library.music import MusicLibraryService
from common.library.youtubedownloader import YouTubeDownloader
   
class piPodGUINavigation(RotaryEncoder, piPodGUI):
    def __init__(self):
#        super().__init__()
        RotaryEncoder.__init__(self)
        piPodGUI.__init__(self)

        self.CurrentScreen = self.configuration.DefaultScreen
        self.CurrentScreenElement = self.configuration.DefaultElement
        self.CurrentScreenElementIndex = 0
        self.PreviousScreen = self.configuration.DefaultScreen
        self.PreviousScreenElement = self.configuration.DefaultElement
        self.ScreenReturnElement = {}
        
        self.setMainScreenElementDefault()
        self.MainScreenShow()
    
    def setMainScreenElementDefault(self):
        if self.CurrentPlaylistId is None or self.CurrentTrackId is None:
            default_element = 'Music'
        else:
            default_element = 'NowPlaying'
    
        self.setCurrentScreenElement(
            'Main',
            default_element
        )
    
        self.markDirty()

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

    def getCurrentListItemWidget(self):
        if self.CurrentScreen == 'AvailablePlaylists':
            item_index = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)
            return self.sPlaylistSelectionList.item_list_container.elements[item_index]
    
        elif self.CurrentScreen == 'PlaylistTracks':
            item_index = self.ScreenNavigation[self.CurrentScreen].index(self.CurrentScreenElement)
            return self.sPlaylistTracks.item_list_container.elements[item_index]
    
        return None
 
    def setPlaylistNavigation(self):
        playlists = list(self.getDownloadedPlaylists(self.CurrentPlaylistId)['Title'])
#        print(f'playlists: {playlists}')
        self.ScreenNavigation['PlaylistTracks'] = playlists
        self.CurrentPlaylistIndex = self.getScreenElementIndex('AvailablePlaylists',  self.CurrentPlaylistInfo.iloc[0]['Playlist'])
        
    def setCurrentScreen(self,  ScreenName):
        # Check id Screen is a configured 
        if ScreenName in self.Screens:
            self.PreviousScreen = self.CurrentScreen
            self.CurrentScreen = ScreenName
        else:
            print('error setting currentScreen')
    
    def setCurrentScreenElement(self, ScreenName, ScreenElement):
        if (
            ScreenName in self.ScreenNavigation
            and ScreenElement in self.ScreenNavigation[ScreenName]
        ):
            self.setCurrentScreen(ScreenName)
    
            self.PreviousScreenElement = (
                self.CurrentScreenElement
            )
    
            self.CurrentScreenElement = ScreenElement
    
            self.CurrentScreenElementIndex = (
                self.ScreenNavigation[ScreenName].index(
                    ScreenElement
                )
            )
    
        else:
            print(
                'error setting currentScreenElement'
            )
            
    def getScreenElementIndex(self, Screen, ScreenElement):
        try:
            return self.ScreenNavigation[Screen].index(ScreenElement)
        except ValueError:
            return 0       
        
    def getCurrentScreenElementIndex(self):
        return self.CurrentScreenElementIndex
        
    def setScreenElementSelected(self, Element):
        match self.CurrentScreen:
            case 'Main' | 'Music':
                self.markDirty()
    
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
                                self.ShowShuffleButtonOff()
                                self.bShuffleOff.select()
                            case 'On':
                                self.ShowShuffleButtonOn()
                                self.bShuffleOn.select()
    
                    case _:
                        pass
    
            case 'AvailablePlaylists' | 'PlaylistTracks' | 'Artists' | 'Albums' | 'Genres' | 'ArtistAlbums' | 'Tools' | 'Import':
                self.markDirty()
    
            case 'OTR':
                pass
    
            case 'Audiobooks':
                pass
    
            case 'Games':
                pass
    
            case 'Settings':
                pass
    
        self.CurrentScreenElement = Element
        self.markDirty()
        
    def setScreenElementUnselected(self, Element):
        match self.CurrentScreen:
            case 'Main' | 'Music':
                self.markDirty()
                    
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
                    
            case 'AvailablePlaylists' | 'PlaylistTracks' | 'Artists' | 'Albums' | 'Genres' | 'ArtistAlbums' | 'Tools' | 'Import':
                self.markDirty()
                    
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
        if IndexCurrentElement > 0:
            self.setScreenElementUnselected(
                self.CurrentScreenElement
            )
    
            self.CurrentScreenElementIndex -= 1
    
            self.CurrentScreenElement = (
                self.ScreenNavigation[
                    self.CurrentScreen
                ][self.CurrentScreenElementIndex]
            )
    
            self.setScreenElementSelected(
                self.CurrentScreenElement
            )

    def NavigateDown(self, IndexCurrentElement):
    
        lengthScreenNavigation = (
            len(
                self.ScreenNavigation[
                    self.CurrentScreen
                ]
            ) - 1
        )
    
        if IndexCurrentElement < lengthScreenNavigation:
            self.setScreenElementUnselected(
                self.CurrentScreenElement
            )
    
            self.CurrentScreenElementIndex += 1
    
            self.CurrentScreenElement = (
                self.ScreenNavigation[
                    self.CurrentScreen
                ][self.CurrentScreenElementIndex]
            )
    
            self.setScreenElementSelected(
                self.CurrentScreenElement
            )
        
    def selectMainScreenElement(self):
        """
        Handle selection behavior for the Main screen.
        """

        self.navigationPath.append('Main')

        match self.CurrentScreenElement:
            case 'NowPlaying':
#                print("1: selecting NowPlaying")
                self.setCurrentScreenElement('NowPlaying', 'Play/Pause')
#                print("2: CurrentScreen =", self.CurrentScreen)
#                print("3: CurrentScreenElement =", self.CurrentScreenElement)
                self.MainScreenHide()
#                print("4: Main hidden")
                self.NowPlayingScreenShow()
#                print("5: NowPlayingScreenShow finished")
                self.setScreenElementSelected(self.CurrentScreenElement)
#                print("6: selection finished")

            case 'Music':
                self.setCurrentScreenElement('Music', 'AvailablePlaylists')
                self.MainScreenHide()
                self.MusicScreenShow()

            case 'OTR':
                pass

            case 'Audiobooks':
                pass

            case 'Games':
                pass

            case 'Tools':
                items = self.ScreenNavigation.get(
                    "Tools",
                    []
                )
            
                if len(items) == 0:
                    return
            
                self.setCurrentScreenElement(
                    "Tools",
                    items[0]
                )
            
                self.MainScreenHide()
                self.ToolsScreenShow()
            
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )
    
    def selectToolsScreenElement(self):
        self.navigationPath.append('Tools')
    
        selectedItem = self.CurrentScreenElement
    
        self.ScreenReturnElement[
            "Tools"
        ] = selectedItem
    
        match selectedItem:
            case 'Import':
                items = self.ScreenNavigation.get(
                    "Import",
                    []
                )
    
                if len(items) == 0:
                    return
    
                self.setCurrentScreenElement(
                    "Import",
                    items[0]
                )
    
                self.ImportScreenShow()
    
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )
            case 'Download':
                self.navigationPath.append(
                    'Tools'
                )
            
                self.setCurrentScreenElement(
                    'Download',
                    'YouTube Playlist'
                )
            
                self.DownloadScreenShow()
            
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )
            
                self.markDirty()
    def selectImportScreenElement(self):
        selectedItem = self.CurrentScreenElement
    
        self.ScreenReturnElement[
            "Import"
        ] = selectedItem
    
        match selectedItem:
            case 'Music':
                print("Starting local music import...")
    
                music_library = MusicLibraryService()
                result = music_library.import_music()
    
                print("Local music import finished.")
                print("Imported:", result["imported"])
                print("Skipped:", result["skipped"])
                print("Errors:", result["errors"])
    
                self.ImportResult = result
    
                self.navigationPath.append('Import')
    
                self.setCurrentScreenElement(
                    "ImportResult",
                    "Back"
                )
    
                self.ImportResultScreenShow()
    
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )
    
                self.markDirty()
    
    def selectMusicScreenElement(self):
        """
        Handle selection behavior for the Music screen.
        """

        self.navigationPath.append('Music')
        self.ScreenReturnElement[
            "Music"
        ] = self.CurrentScreenElement

        match self.CurrentScreenElement:
            case 'AvailablePlaylists':
#                print(f"self.CurrentPlaylistInfo: {self.CurrentPlaylistInfo},  {type(self.CurrentPlaylistInfo)}")

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
                albums = list(
                    self.getAlbumsFromDB()["Album"]
                )
            
                self.ScreenNavigation[
                    "Albums"
                ] = albums
            
                if len(albums) == 0:
                    return
            
                self.setCurrentScreenElement(
                    "Albums",
                    albums[0]
                )
            
                self.MusicScreenHide()
                self.AlbumsScreenShow()
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )

            case 'Artists':
                artists = list(
                    self.getArtistsFromDB()["Artist"]
                )
            
                self.ScreenNavigation[
                    "Artists"
                ] = artists
            
                if len(artists) == 0:
                    return
            
                self.setCurrentScreenElement(
                    "Artists",
                    artists[0]
                )
            
                self.MusicScreenHide()
                self.ArtistsScreenShow()
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )

            case 'Genres':
                genres = list(
                    self.getGenresFromDB()["Genre"]
                )
            
                self.ScreenNavigation[
                    "Genres"
                ] = genres
            
                if len(genres) == 0:
                    return
            
                self.setCurrentScreenElement(
                    "Genres",
                    genres[0]
                )
            
                self.MusicScreenHide()
                self.GenresScreenShow()
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )

            case _:
                pass
    
    def selectDownloadScreenElement(self):
        selectedItem = self.CurrentScreenElement
    
        match selectedItem:
            case 'YouTube Playlist':
                downloader = YouTubeDownloader()
    
                playlists = downloader.getLibraryPlaylistsFromYouTube()
    
                if len(playlists) == 0:
                    print("No YouTube playlists found.")
                    return
    
                self.YouTubePlaylists = playlists
    
                playlist_titles = [
                    playlist['title']
                    for playlist in playlists
                ]
    
                self.ScreenNavigation[
                    "YouTubePlaylists"
                ] = playlist_titles
    
                self.navigationPath.append(
                    'Download'
                )
    
                self.setCurrentScreenElement(
                    "YouTubePlaylists",
                    playlist_titles[0]
                )
    
                self.YouTubePlaylistsScreenShow()
    
                self.setScreenElementSelected(
                    self.CurrentScreenElement
                )
    
                self.markDirty()
    
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
#        print(f'tracks: {tracks}')

        self.ScreenNavigation['PlaylistTracks'] = tracks
        self.setCurrentScreenElement('PlaylistTracks', tracks[trackIndex])

#        print(f'self.CurrentScreenElement: {self.CurrentScreenElement}')

        self.AvailablePlaylistsScreenHide()
        self.PlaylistTracksScreenShow()
        self.setScreenElementSelected(self.CurrentScreenElement)
    
    def selectArtist(self):
        self.navigationPath.append('Artists')
    
        selectedArtist = self.CurrentScreenElement

        self.ScreenReturnElement[
            "Artists"
        ] = selectedArtist

        self.CurrentArtist = selectedArtist
        
        dfAlbums = self.getAlbumsByArtistFromDB(
            selectedArtist
        )
    
        albums = ["All Tracks"]
    
        if not dfAlbums.empty:
            albums.extend(
                list(dfAlbums["Album"])
            )
    
        self.ScreenNavigation[
            "ArtistAlbums"
        ] = albums
    
        self.setCurrentScreenElement(
            "ArtistAlbums",
            albums[0]
        )
    
        self.ArtistAlbumsScreenShow()
    
        self.setScreenElementSelected(
            self.CurrentScreenElement
        )
    
    def openTrackList(self, dfTracks, queue_id, queue_name):
        if dfTracks.empty:
            return
    
        self.setCurrentTrackList(
            dfTracks,
            queue_id,
            queue_name
        )
    
        tracks = list(
            dfTracks["Title"]
        )
    
        self.ScreenNavigation[
            "PlaylistTracks"
        ] = tracks
    
        self.setCurrentScreenElement(
            "PlaylistTracks",
            tracks[0]
        )
    
        self.PlaylistTracksScreenShow()
    
        self.setScreenElementSelected(
            self.CurrentScreenElement
        )
    
    def selectAlbum(self):
        self.navigationPath.append('Albums')
    
        selectedAlbum = self.CurrentScreenElement

        self.ScreenReturnElement[
            "Albums"
        ] = selectedAlbum
    
        dfTracks = self.getTracksByAlbumFromDB(
            selectedAlbum
        )
    
        if dfTracks.empty:
            return
    
        album_id = dfTracks.iloc[0]['AlbumId']
    
        queue_id = "album:" + str(album_id)
    
        self.openTrackList(
            dfTracks,
            queue_id,
            selectedAlbum
        )
    
    def selectArtistAlbum(self):
        self.navigationPath.append('ArtistAlbums')
    
        selectedItem = self.CurrentScreenElement

        self.ScreenReturnElement[
            "ArtistAlbums"
        ] = selectedItem
    
        if selectedItem == "All Tracks":
            dfTracks = self.getTracksByArtistFromDB(
                self.CurrentArtist
            )
    
            queue_id = "artist:" + self.CurrentArtist
            queue_name = self.CurrentArtist
    
        else:
            dfTracks = self.getTracksByArtistAndAlbumFromDB(
                self.CurrentArtist,
                selectedItem
            )
    
            if dfTracks.empty:
                return
    
            album_id = dfTracks.iloc[0]["AlbumId"]
    
            queue_id = "album:" + str(album_id)
            queue_name = selectedItem
    
        self.openTrackList(
            dfTracks,
            queue_id,
            queue_name
        )
        
    def selectGenre(self):
        self.navigationPath.append('Genres')
    
        selectedGenre = self.CurrentScreenElement

        self.ScreenReturnElement[
            "Genres"
        ] = selectedGenre
    
        dfTracks = self.getTracksByGenreFromDB(
            selectedGenre
        )
    
        queue_id = "genre:" + selectedGenre
    
        self.openTrackList(
            dfTracks,
            queue_id,
            selectedGenre
        )
    
    def selectPlaylistTrack(self):
        """
        Handle selection behavior for the Playlist Tracks screen.
        """

        self.navigationPath.append('PlaylistTracks')

        selectedTrack = self.CurrentScreenElement

        self.setCurrentScreenElement('NowPlaying', 'Play/Pause')

        selectedTrackId = self.getTrackIdFromCurrentPlaylistByTitle(
            selectedTrack
        )
        if selectedTrackId is None:
            return

        self.setSelectedTrack(selectedTrackId)

        self.PlaylistTracksScreenHide()
        self.NowPlayingScreenShow()
        self.setScreenElementSelected(self.CurrentScreenElement)
    
    def selectYouTubePlaylist(self):
        selected_title = self.CurrentScreenElement
    
        selected_playlist = None
    
        for playlist in self.YouTubePlaylists:
            if playlist['title'] == selected_title:
                selected_playlist = playlist
                break
    
        if selected_playlist is None:
            print(
                "Could not find YouTube playlist:",
                selected_title
            )
            return
    
        playlist_id = selected_playlist['id']
    
        print(
            "Downloading YouTube playlist:",
            selected_title
        )
    
        downloader = YouTubeDownloader()
    
        downloader.downloadPlaylistFromYouTube(
            playlist_id
        )
    
        print(
            "YouTube playlist download finished:",
            selected_title
        )
    
    def hideCurrentScreen(self):
        """
        Hide whichever screen is currently active.
    
        This keeps screen-hiding behavior in one place and reuses the existing
        generic hide(ScreenName) method from piPodGUI.
        """
    
        self.hide(self.CurrentScreen)
        
    def showMusicFromBack(self):
        return_element = self.ScreenReturnElement.get(
            "Music",
            "AvailablePlaylists"
        )
    
        self.setCurrentScreenElement(
            'Music',
            return_element
        )
    
        self.MusicScreenShow()

    def showDirectListFromBack(
        self,
        screen_name,
        items,
        show_method
    ):
        self.ScreenNavigation[
            screen_name
        ] = items
    
        if len(items) == 0:
            return
    
        return_item = self.ScreenReturnElement.get(
            screen_name,
            items[0]
        )
    
        if return_item not in items:
            return_item = items[0]
    
        self.setCurrentScreenElement(
            screen_name,
            return_item
        )
    
        show_method()
    
        self.setScreenElementSelected(
            self.CurrentScreenElement
        )

    def showArtistsFromBack(self):
        artists = list(
            self.getArtistsFromDB()["Artist"]
        )
    
        self.showDirectListFromBack(
            "Artists",
            artists,
            self.ArtistsScreenShow
        )

    def showAlbumsFromBack(self):
        albums = list(
            self.getAlbumsFromDB()["Album"]
        )
    
        self.showDirectListFromBack(
            "Albums",
            albums,
            self.AlbumsScreenShow
        )

    def showArtistAlbumsFromBack(self):
        items = self.ScreenNavigation.get(
            "ArtistAlbums",
            []
        )
    
        self.showDirectListFromBack(
            "ArtistAlbums",
            items,
            self.ArtistAlbumsScreenShow
        )

    def showGenresFromBack(self):
        genres = list(
            self.getGenresFromDB()["Genre"]
        )
    
        self.showDirectListFromBack(
            "Genres",
            genres,
            self.GenresScreenShow
        )

    def showToolsFromBack(self):
        items = self.ScreenNavigation.get(
            "Tools",
            []
        )
    
        self.showDirectListFromBack(
            "Tools",
            items,
            self.ToolsScreenShow
        )
    
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
        
    def showAvailablePlaylistsFromBack(self):
        """
        Restore the Available Playlists screen after Back navigation.
        """
    
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

    def showPlaylistTracksFromBack(self):
        tracks = self.ScreenNavigation.get(
            "PlaylistTracks",
            []
        )
    
        if len(tracks) == 0:
            tracks = list(
                self.getPlaylistTracks(
                    self.CurrentPlaylistId
                )["Title"]
            )
    
            self.ScreenNavigation[
                "PlaylistTracks"
            ] = tracks
    
        if len(tracks) == 0:
            return
    
        self.setCurrentScreenElement(
            "PlaylistTracks",
            tracks[0]
        )
    
        self.drawPlaylistTracksDirect()
    
    def goBack(self):
        """
        Return to the previous screen using navigationPath.

        This centralizes Back behavior so the Now Playing Back button and
        future rotary Left button can use the same path.
        """

#        print("Back from screen:", self.CurrentScreen)
#        print("navigationPath before back:", self.navigationPath)

        if len(self.navigationPath) == 0:
            print("No previous screen. Staying on current screen.")
            return

        previous_screen = self.navigationPath.pop()

        self.setScreenElementUnselected(self.CurrentScreenElement)
        self.hideCurrentScreen()
        
        match previous_screen:
            case 'Main':
                return_element = self.ScreenReturnElement.get(
                    "Main",
                    self.CurrentScreen
                )

                self.setCurrentScreenElement(
                    'Main',
                    return_element
                )

                self.MainScreenShow()

            case 'Music':
                self.showMusicFromBack()

            case 'AvailablePlaylists':
                self.showAvailablePlaylistsFromBack()

            case 'PlaylistTracks':
                self.showPlaylistTracksFromBack()
            
            case 'Albums':
                self.showAlbumsFromBack()
                
            case 'Artists':
                self.showArtistsFromBack()
            
            case 'ArtistAlbums':
                self.showArtistAlbumsFromBack()
                    
            case 'Genres':
                self.showGenresFromBack()    
                
            case 'Tools':
                self.showToolsFromBack()
                
            case _:
                print("Back target not implemented:", previous_screen)

#        print("navigationPath after back:", self.navigationPath)
        
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
            
            case 'ImportResult':
                self.goBack()
            
            case 'Tools':
                self.selectToolsScreenElement()
                
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
            case 'Artists':
                self.selectArtist()
            case 'ArtistAlbums':
                self.selectArtistAlbum()
            case 'Albums':
                self.selectAlbum()
            case 'Genres':
                self.selectGenre()
            case 'Tools':
                self.selectToolsScreenElement()
            case 'Import':
                self.selectImportScreenElement()
            case 'Download':
                self.selectDownloadScreenElement()
            case 'YouTubePlaylists':
                self.selectYouTubePlaylist()
                
    def EncoderNavigation(self, EncoderActivity):
#        print(f'EncoderActivity: {EncoderActivity}')
#        print(f'CurrentScreenElement: {self.CurrentScreenElement}')
        control = next(iter(EncoderActivity))
        controlAction = EncoderActivity[control]
        indexCurrentElement = (self.CurrentScreenElementIndex)
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
