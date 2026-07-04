# Refactor Notes

## Refactor Direction

The current app works as a hardware/software prototype, but the code is not yet structured in a way that makes new features easy to add.

The next phase should not focus on small tactical edits inside the existing GUI code. The better approach is to build a more supportable foundation under the current app, then migrate the UI onto that foundation.

The main idea:

* Do not start by untangling pygame screens.
* Start by extracting the non-UI services that the screens depend on.
* Build and test foundational services without the UI.
* Move existing working code into clearer service boundaries where possible.
* Rework messy code only when the service boundary requires it.
* Leave fragile pygame/PiTFT display behavior alone until the rest of the app is better structured.

## Current Problem

The app is simple in features, but the current code mixes too many responsibilities.

Current issues:

* GUI code controls too much application behavior.
* Navigation code directly manipulates GUI widgets and playback actions.
* Database state, playback state, screen state, and widget state are tightly coupled.
* `pipodgui.py` owns too much:

  * pygame display setup
  * pygame_gui widgets
  * screen show/hide behavior
  * track metadata loading
  * album artwork loading
  * playback commands
  * playback position updates
  * database writes
  * dirty/redraw state
* `pipodgui_navigation.py` is not just navigation:

  * it reads input behavior
  * changes selected widgets
  * changes screens
  * dispatches playback commands
  * acts like an application controller
* Small changes can break unrelated behavior.
* Recent helper extraction inside `pipodgui.py` did not really move the architecture forward because it kept the same hidden dependencies inside the GUI class.

## Important Decision

Do not continue trying to clean up pygame display refresh directly right now.

The current PiTFT display path is fragile. Direct `pygame.display.flip()` calls may look wrong architecturally, but removing them caused display failure.

For now:

* Leave display refresh mostly as-is.
* Accept the once-per-second playback position redraw.
* Do not attempt partial redraws yet.
* Do not remove direct pygame display calls yet.
* Do not start the refactor from the UI rendering layer.

## Refactor Strategy

Use a bottom-up service refactor.

General order:

1. Define the foundation services.
2. Decide exactly what each service owns.
3. Find the existing code that already performs those functions.
4. Move appropriate code with minimal behavior change.
5. Rework only code that does not fit the new boundary.
6. Build UI screens on top of the services.
7. Add application controller glue.
8. Replace or simplify the current main loop last.

This keeps the fragile UI working while supportable non-UI pieces are built beside it.

## Target Shape

These boundaries are provisional and can be adjusted as the code becomes clearer.

* `piPod.py`

  * starts the app
  * runs the main loop
  * passes input/events to an application controller
  * does not know individual UI widgets

* Input layer

  * reads rotary encoder
  * reads PiTFT buttons
  * reads side volume buttons
  * emits simple input events

* Application controller

  * receives input events
  * decides what action happens
  * owns high-level app flow
  * coordinates playback, library, and UI state

* Playback service

  * play
  * pause
  * next
  * previous
  * current position
  * duration
  * volume

* Library service

  * playlists
  * albums
  * genres
  * tracks
  * metadata
  * saved current track/playlist state

* UI state

  * current screen
  * selected item
  * current track display info
  * playback status
  * progress info

* UI renderer

  * owns pygame/pygame_gui widgets
  * renders UI state
  * does not decide app behavior

## Foundation Service Order

Suggested order:

1. Library service
2. Playback service
3. Input service
4. App/UI state objects
5. Application controller
6. UI renderer/screens
7. Main loop

Reasoning:

* Library service is the safest starting point because it is mostly data access and metadata lookup.
* Library service can be tested without pygame, hardware, audio, or the PiTFT.
* Playback service is next because audio behavior already exists, but needs clearer boundaries.
* Input service is already partially separated through the rotary encoder code.
* State objects should reflect what the services actually need to share.
* Application controller should come after the services are clearer.
* UI rendering should come later because the display path is fragile.

## Library Service

Responsibilities:

* playlists
* tracks
* albums
* genres
* track metadata
* artwork lookup/loading
* saved current playlist
* saved current track
* saved playback position

Does not own:

* pygame widgets
* screen transitions
* play/pause behavior
* selected UI element
* rotary navigation behavior

Existing code likely comes from:

* `common/library/database.py`
* parts of `common/pipodgui.py`
* possibly `getTrackID3Tags()` from `common/audio/player.py`

Important design question:

* ID3 metadata lookup probably belongs in the Library service, not the Playback service.

Possible public methods:

```python
library.get_downloaded_playlists()
library.get_playlist_tracks(playlist_id)
library.get_track(track_id)
library.get_current_track()
library.set_current_track(track_id, duration_seconds=None, position_seconds=0)
library.get_track_metadata(track_id)
library.get_current_playlist()
library.set_current_playlist(playlist_id)
```

First possible implementation step:

* Create `common/library/service.py`.
* Create a `LibraryService` class that wraps existing `MusicDB`.
* Do not change the app to use it yet.
* Test it separately from a command-line script.

## Playback Service

Responsibilities:

* load/set active audio track
* play
* pause
* stop if needed
* current playback position
* duration if provided by the audio backend
* volume

Possible responsibility, but needs care:

* next/previous should probably play a specified track
* playlist ordering and deciding which track is next should not belong here

Does not own:

* playlist ordering
* shuffle list generation
* repeat policy
* track metadata display
* database queries
* pygame UI
* selected screen or selected widget

Existing code likely comes from:

* `common/audio/player.py`
* playback command methods currently in `common/pipodgui.py`

Important boundary:

* Playback service plays a track.
* Application controller decides which track should be played.

## Input Service

Responsibilities:

* rotary wheel movement
* rotary button press
* PiTFT buttons
* side volume buttons
* convert hardware activity into simple input events

Does not own:

* screen navigation rules
* play/pause decisions
* current selected widget
* pygame rendering

Existing code likely comes from:

* `common/input/rotary.py`
* future PiTFT button code
* future side volume button code

Possible input events:

```python
InputEvent("UP")
InputEvent("DOWN")
InputEvent("SELECT")
InputEvent("BACK")
InputEvent("HOME")
InputEvent("NEXT")
InputEvent("PREVIOUS")
InputEvent("VOLUME_UP")
InputEvent("VOLUME_DOWN")
```

## State

There are probably two categories of state.

Persistent state:

* current playlist
* current track
* playback position
* maybe shuffle/repeat later

Runtime UI/app state:

* current screen
* selected item
* playback status
* current display track info
* progress info

Persistent state probably belongs to the Library service or a small persistence service.

Runtime state should be plain Python objects, not pygame widgets.

## Application Controller

Responsibilities:

* receives input events
* decides what action happens
* applies navigation rules
* coordinates library and playback services
* updates UI/app state

Does not own:

* pygame drawing
* direct button widgets
* raw hardware polling
* low-level database queries
* low-level audio backend details

The controller is glue logic, but it should come after the services are clearer.

## UI Renderer

Responsibilities:

* owns pygame/pygame_gui widgets
* builds screens
* applies UI state to widgets
* performs existing display update behavior
* marks/redraws display as needed

Does not own:

* playlist decisions
* audio backend behavior
* library/database queries
* raw hardware input
* application flow decisions

Important note:

* Keep the current pygame/PiTFT display behavior mostly intact until the renderer boundary is clearer.
* Do not start the refactor here.

## Lessons From Recent Refactor Attempt

The `loadCurrentTrackDisplayState()` helper was not the right direction.

Problems:

* It stayed inside the overloaded GUI class.
* It depended on hidden current database state.
* It did not create a real service boundary.
* It rearranged code without meaningfully separating responsibilities.
* It caused failures when the saved current track state was invalid or unexpected.

Better future direction:

* Track metadata loading should be handled by a Library service.
* The method should accept explicit input, such as `track_id`.
* It should return plain data, not directly update pygame widgets.
* GUI code should apply already-prepared state to widgets.

Example future shape:

```python
track_info = library.get_track_display_info(track_id)
ui_state.current_track = track_info
renderer.render(ui_state)
```

## Playback State Lesson

The app stores current playlist, current track, and playback position in the database.

During refactoring, code changes may leave saved current-track state pointing at an invalid or incomplete track record.

Observed failure mode:

* Now Playing can fail in `getTrackID3Tags()` with `KeyError: 'FileLocation'`.
* Re-selecting a track from the library can restore valid current-track state.

This means:

* Not every Now Playing failure is necessarily a code failure.
* Saved playback state can become invalid during refactor.
* Service boundaries should make this state easier to validate and recover.

## Things To Avoid For Now

* Do not remove `pygame.display.flip()` calls.
* Do not attempt partial redraws.
* Do not add new user-facing features yet.
* Do not rewrite the full GUI at once.
* Do not make helpers that depend on hidden current database state.
* Do not chase every typo yet.
* Do not remove debug `print()` calls until the code structure is more stable.

## Next Practical Step

Start with the Library service.

First small session:

* Review `common/library/database.py`.
* Identify which current methods are pure library/database responsibilities.
* Create `common/library/service.py`.
* Add a `LibraryService` class that wraps existing `MusicDB`.
* Move or wrap one simple method first, likely playlist lookup.
* Test from a small command-line script.
* Do not wire the UI to it yet.

Goal of the first step:

* Prove that a foundation service can be created and tested without touching pygame, PiTFT display behavior, or navigation code.
