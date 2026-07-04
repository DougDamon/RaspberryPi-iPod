# Current Code Inventory

## Purpose

This document captures the current state of the RaspberryPi-iPod codebase before deeper UI refactoring.

The goal is to understand what the current code does, especially around screen refresh, navigation, playback state, and input handling.

## Display Redraw Behavior

The GUI now uses a dirty/redraw flag so the main loop does not redraw continuously.

Current behavior:
- The main loop updates `pygame_gui` every loop.
- The display is redrawn only when the GUI is marked dirty.
- Navigation changes mark the GUI dirty.
- Screen changes mark the GUI dirty.
- Playback position updates are throttled to once per second.
- Playback position updates currently still use the normal dirty redraw path.

Current limitation:
- Playback position no longer causes constant flicker.
- A noticeable once-per-second redraw can still occur while music is playing.
- A future improvement should update only the Now Playing time/progress area instead of redrawing the full display.

Relevant files:
- `piPod.py` controls when redraws happen in the main loop.
- `common/pipodgui.py` owns dirty/redraw state and display update methods.
- `common/pipodgui_navigation.py` marks the GUI dirty after navigation and selection changes.
- 
## Entry Point

### `piPod.py`

Responsibilities:
- Creates the global configuration object.
- Creates the music database object.
- Creates the main GUI/navigation object.
- Gets the pygame clock from the GUI object.
- Runs the main application loop.
- Reads rotary encoder activity through the GUI/navigation object.
- Sends encoder activity into UI navigation.
- Reads pygame/gui events.
- Dispatches button events.
- Dispatches playlist/track selection events.
- Handles music-end events.
- Updates current playback position.
- Updates pygame_gui manager.
- Updates pygame_gui manager every loop.
- Redraws/updates the display only when the GUI is marked dirty.
- Quits the GUI system on shutdown.

Current dependencies:
- `common.config.settings.piPodConfiguration`
- `common.pipodgui_navigation`
- `common.library.database.MusicDB`

Important state currently stored in `piPod.py`:
- `is_running`
- `isMusicPlaying`
- `isMusicPaused`
- `currentPosition`
- `CurrentPlaylistId`
- `CurrentTrackId`
- `NextTrackSet`
- `SelectedNowPlayingPlaylistId`
- `SelectedNowPlayingTrackId`

Possible problems:
- `piPod.py` directly knows about many individual UI elements.
- `piPod.py` directly dispatches screen transitions.
- Playback state is split between local variables and the GUI object.
- `piPod.py` calls GUI methods that also appear to control audio playback.
- Event handling, playback updates, and rendering are still mixed in the same loop.
- Playback state is split between local variables and the GUI object.
- See [Display Redraw Behavior](#display-redraw-behavior).
- Event handling, playback updates, and rendering are all mixed in the same loop.
- The name `piPodGUI` is reused first as a module alias and then as an object instance, which makes the code harder to reason about.

UI refresh observations:
- The main loop runs at 60 FPS:
  `clock.tick(60)`
- Every loop calls:
  `piPodGUI.manager.update(time_delta)`
- Every loop calls:
  `piPodGUI.drawScreen()`
- Every loop calls:
  `piPodGUI.updateDisplay()`

This strongly supports the suspected issue:
- Arbitrary and constant screen refreshes
- No clear dirty/needs-redraw flag

## Main GUI

### `common/pipodgui.py`

Responsibilities:
- Defines `piPodGUI`.
- Initializes pygame display/window.
- Initializes pygame_gui UI manager.
- Loads configuration.
- Loads theme file.
- Creates all major UI windows:
  - Main
  - Now Playing
  - Music
  - Available Playlists
  - Playlist Tracks
- Creates buttons, labels, selection lists, album art image, and progress bar widgets.
- Shows and hides screens.
- Draws the UI.
- Updates the physical display.
- Reads pygame events.
- Provides pygame clock.
- Tracks current playlist and track.
- Loads current track metadata and album artwork.
- Updates now-playing labels.
- Updates playback position display.
- Updates progress bar.
- Controls play/pause/next/previous behavior.
- Controls repeat and shuffle UI state.
- Calls audio playback methods.
- Calls music database methods.
- Updates current track position in the database.

Current dependencies:
- `pygame`
- `pygame_gui`
- `PIL.Image`
- `common.config.settings.piPodConfiguration`
- `common.audio.player.AudioPlayback`
- `common.library.database.MusicDB`

Important inheritance:
- `piPodGUI(AudioPlayback, MusicDB)`

This means `piPodGUI` directly inherits audio playback behavior and database behavior.

Important state:
- `configuration`
- `Screens`
- `ScreenNavigation`
- `window_surface`
- `background`
- `manager`
- `windowMainScreen`
- `windowNowPlaying`
- `windowMusic`
- `windowAvailablePlaylists`
- `windowPlaylistTracks`
- `CurrentPlaylistId`
- `CurrentPlaylistInfo`
- `CurrentTrackId`
- `NextPlaylistId`
- `NextTrackId`
- `AutoPlayOnStart`
- `CurrentAlbumArt`
- `CurrentTitle`
- `CurrentArtist`
- `CurrentAlbum`
- `CurrentGenre`
- `CurrentPlaylist`
- `CurrentPosition`
- `CurrentPositionPercent`
- `StartPlaybackPosition`
- `CurrentPositionFormat`
- `CurrentDurationSeconds`
- `CurrentDurationFormat`
- `MusicScreenInit`
- `AvailablePlaylistsScreenInit`
- `navigationPath`

Screen methods:
- `MainScreen`
- `MainScreenShow`
- `MainScreenHide`
- `NowPlayingScreen`
- `NowPlayingScreenShow`
- `NowPlayingScreenHide`
- `MusicScreen`
- `MusicScreenShow`
- `MusicScreenHide`
- `AvailablePlaylistsScreen`
- `AvailablePlaylistsScreenShow`
- `AvailablePlaylistsScreenHide`
- `PlaylistTracksScreen`
- `PlaylistTracksScreenShow`
- `PlaylistTracksScreenHide`
- `show`
- `hide`

Playback/UI methods:
- `Play`
- `Pause`
- `ShowPlayButton`
- `ShowPauseButton`
- `NextTrackNowPlaying`
- `PreviousTrackNowPlaying`
- `updateCurrentPosition`
- `resetCurrentPosition`

Repeat/shuffle methods:
- `ShowRepeatButtonOff`
- `ShowRepeatButtonOn`
- `ShowRepeatButtonOne`
- `RepeatOff`
- `RepeatOn`
- `RepeatOne`
- `ShowShuffleButtonOff`
- `ShowShuffleButtonOn`
- `ShuffleOff`
- `ShuffleOn`

Library helper methods:
- `getAvailablePlaylists`
- `getPlaylistTracks`
- `setSelectedTrack`
- `setNextTrack`
- `setPreviousTrack`

Display/event methods:
- `getClock`
- `getEvent`
- `drawScreen`
- `updateDisplay`
- `quit`

Possible problems:
- GUI, audio, and database behavior are tightly coupled through inheritance.
- The GUI owns playback state.
- The GUI owns current track metadata.
- The GUI owns screen state and widget state.
- The GUI directly updates database playback position.
- The GUI directly controls playback commands.
- The GUI loads and resizes album artwork inside screen show/change methods.
- Now-playing screen update logic is duplicated in `NowPlayingScreenShow`, `NextTrackNowPlaying`, and `PreviousTrackNowPlaying`.
- Screen construction and screen display are mixed together.
- Some methods both change state and redraw/update widgets.
- Some methods may still contain direct display-update behavior from the earlier implementation.
- Display redraw is now mostly controlled through the dirty flag, but older direct draw/update calls should be reviewed during future cleanup.
- Playback position updates are throttled to once per second but still use the normal dirty redraw path.
- See [Display Redraw Behavior](#display-redraw-behavior).
- `window_surface.blit(self.background, ...)` appears in multiple places, which may contribute to inconsistent clearing/redrawing.
- The typo `NoAblumArt` appears in variable names.
- `formatTrackTime` references `self.Seconds` in the hour+ case, which may be a bug.
- `setUISelectionListButtonTheme` loops directly over `UISelectionList.item_list_container`, which may be fragile depending on pygame_gui internals.
- Several methods contain debug `print()` calls.
- `CurrentTrackid` appears with a lowercase `i` in one place, which may be a typo separate from `CurrentTrackId`.

UI refresh notes:
- Owns the dirty/redraw state.
- Owns `drawScreen()` and `updateDisplay()`.
- `updateCurrentPosition()` updates elapsed time/progress and marks the GUI dirty once per displayed second.
- See [Display Redraw Behavior](#display-redraw-behavior).

This supports the known suspected causes:
- Arbitrary and constant screen refreshes
- No clear dirty/needs-redraw flag
- Partial updates and full redraws mixed together
- Drawing logic mixed with state changes
- Playback state changes not consistently propagated to UI

## UI Navigation

### `common/pipodgui_navigation.py`

Responsibilities:
- Defines `piPodGUINavigation`.
- Inherits from both `RotaryEncoder` and `piPodGUI`.
- Initializes rotary encoder hardware.
- Initializes the GUI.
- Stores current screen and current screen element.
- Stores previous screen and previous screen element.
- Selects default main screen element.
- Handles directional navigation.
- Handles select/press behavior.
- Changes selected/unselected visual UI state.
- Switches between screens.
- Updates screen navigation lists dynamically for playlists and tracks.
- Dispatches now-playing actions such as play, pause, next, previous, repeat, and shuffle.
- Calls database/library methods through inherited GUI state.
- Calls audio/playback methods through inherited GUI state.

Current dependencies:
- `common.pipodgui.piPodGUI`
- `common.input.rotary.RotaryEncoder`

Important state:
- `CurrentScreen`
- `CurrentScreenElement`
- `PreviousScreen`
- `PreviousScreenElement`
- `ScreenNavigation`
- `Screens`
- `navigationPath`
- `CurrentPlaylistId`
- `CurrentTrackId`
- `CurrentPlaylistInfo`
- `AudioPlaying`
- `Repeat`
- `Shuffle`

Possible problems:
- Multiple inheritance combines hardware input and GUI behavior into one object.
- Navigation logic directly manipulates UI widgets.
- Navigation logic directly calls playback commands.
- Navigation logic directly changes screens.
- Navigation logic depends heavily on string names such as `Main`, `NowPlaying`, `Music`, `AvailablePlaylists`, and `PlaylistTracks`.
- Selection state and screen state are manually synchronized.
- Some screen navigation lists are generated dynamically, which may make state harder to reason about.
- Back navigation appears incomplete or fragile.
- `trackIndex` is referenced in the `NowPlaying` back action but does not appear to be defined in that scope.
- Debug `print()` calls are scattered throughout the navigation flow.
- This module is currently closer to an application controller than a pure navigation module.

UI refresh observations:
- Selecting or unselecting an element immediately changes widget state.
- Screen show/hide calls happen inside navigation methods.
- Navigation and selection changes should mark the GUI dirty after visible state changes.
- This module participates in the redraw flow described in [Display Redraw Behavior](#display-redraw-behavior).

## Input

### `common/input/rotary.py`

Responsibilities:
- Reads rotary wheel movement
- Reads hardware button press/release state
- Returns simple event dictionaries

Notes:
- Good subsystem boundary
- Later improvement: convert dictionary output into formal input events

## Audio

### `common/audio/player.py`

Responsibilities:
- Current audio playback implementation
- Still uses current backend

Notes:
- Future goal: create backend-neutral audio interface
- Later backend may be VLC, MPD, GStreamer, or similar

## Library

### `common/library/database.py`

Responsibilities:
- Music database access
- Track/library/playlist data

Notes:
- Future goal: support media types beyond music
- Future goal: scanner/importer and metadata enrichment

## Configuration

### `common/config/settings.py`

Responsibilities:
- Loads config file
- Provides paths/settings to the rest of the app
- Creates work directory

Notes:
- Already moved successfully

## UI Refresh Status

Current stable behavior:

* [x] Main loop no longer redraws the display continuously.
* [x] GUI dirty/redraw flag exists.
* [x] Navigation and selection changes now request redraws.
* [x] Playback position updates are throttled to once per displayed second.
* [x] Constant playback flicker has been reduced.

Still known:

* [x] A once-per-second redraw is still noticeable while music is playing.
* [ ] Playback position currently uses the normal full-screen dirty redraw path.
* [ ] Partial updates and full redraws are still mixed together.
* [ ] Playback position should eventually update only the Now Playing time/progress area.
* [ ] Some older direct display-update calls may still exist and should be reviewed.

Future cleanup:

* Centralize all display updates through one redraw path.
* Remove or replace older direct `pygame.display.flip()` calls.
* Separate state changes from drawing/display-update calls where practical.


