"""
UI action names for the piPod application.

This module defines the vocabulary for user-interface actions such as
opening screens, selecting items, controlling playback, and handling
global controls.

These actions do not perform any behavior by themselves. They are intended
to give the future UI/controller layer clear names for what the user is
trying to do, without tying that intent directly to pygame widgets,
rotary encoder details, or playback/database code.
"""

from enum import Enum


class UIAction(Enum):
    # Screen navigation
    OPEN_MAIN = "open_main"
    OPEN_NOW_PLAYING = "open_now_playing"
    OPEN_MUSIC = "open_music"
    OPEN_PLAYLISTS = "open_playlists"
    OPEN_PLAYLIST_TRACKS = "open_playlist_tracks"

    # Selection actions
    SELECT_PLAYLIST = "select_playlist"
    SELECT_TRACK = "select_track"

    # Playback actions
    PLAY_PAUSE = "play_pause"
    PLAY = "play"
    PAUSE = "pause"
    NEXT_TRACK = "next_track"
    PREVIOUS_TRACK = "previous_track"

    # Playback modes
    TOGGLE_SHUFFLE = "toggle_shuffle"
    CYCLE_REPEAT = "cycle_repeat"

    # General navigation
    BACK = "back"
    HOME = "home"

    # Future/global controls
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
