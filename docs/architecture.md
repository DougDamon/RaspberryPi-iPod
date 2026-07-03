
## Current Refactored Structure

- `piPod.py`
  - Application entry point
  - Main loop
  - Creates GUI, audio, database, and input objects

- `common/config/settings.py`
  - Loads config file
  - Provides paths and configuration values

- `common/input/rotary.py`
  - Reads rotary encoder and button activity

- `common/audio/player.py`
  - Current audio playback implementation

- `common/library/database.py`
  - Music library/database access

- `common/pipodgui.py`
  - Main UI object
  - Drawing
  - Current screen state
  - Playback-related UI behavior
  - Navigation integration

- `common/pipodgui_navigation.py`
  - UI navigation rules/state