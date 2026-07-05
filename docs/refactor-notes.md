## UI Refactor Focus

The main refactor problem is the UI.

The goal is to make the UI understandable before adding new features.

### Screens

- Main
- Now Playing
- Music
- Available Playlists
- Playlist Tracks

### Main Screen Actions

- Now Playing → show Now Playing screen
- Music → show Music screen
- OTR → placeholder
- Audiobooks → placeholder
- Games → placeholder
- Settings/Management → placeholder

### Now Playing Actions

- Shuffle → toggle shuffle
- Repeat → cycle repeat mode
- Rewind → previous/restart track
- Play/Pause → toggle playback
- Forward → next track
- Back → previous screen
- Home → main screen

### Music Screen Actions

- Playlists → show Available Playlists
- Albums → placeholder
- Artists → placeholder
- Genres → placeholder

### Available Playlists Actions

- Select playlist → set current playlist and show Playlist Tracks

### Playlist Tracks Actions

- Select track → set current track and show Now Playing

## UI Actions

UI actions are named commands that describe what the interface wants to do.

They do not perform the action directly. They are vocabulary for the future controller layer.

Initial actions are defined in:

- `common/ui/actions.py`