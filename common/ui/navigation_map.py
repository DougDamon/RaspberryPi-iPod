"""
Screen element to UI action mapping.

The current UI navigation code uses screen names and element names as strings.
This module starts centralizing what those screen elements mean in terms of
application actions.

It does not perform navigation or execute actions. It only maps existing
screen/element names to UIAction values so future controller code can use
named actions instead of hard-coded strings spread through the UI.
"""

from common.ui.actions import UIAction


SCREEN_ELEMENT_ACTIONS = {
    "Main": {
        "NowPlaying": UIAction.OPEN_NOW_PLAYING,
        "Music": UIAction.OPEN_MUSIC,
        "OTR": None,
        "Audiobooks": None,
        "Games": None,
        "Settings": None,
        "Management": None,
    },
    "NowPlaying": {
        "Shuffle": UIAction.TOGGLE_SHUFFLE,
        "Repeat": UIAction.CYCLE_REPEAT,
        "Rewind": UIAction.PREVIOUS_TRACK,
        "Play/Pause": UIAction.PLAY_PAUSE,
        "Forward": UIAction.NEXT_TRACK,
        "Back": UIAction.BACK,
        "Home": UIAction.HOME,
    },
    "Music": {
        "AvailablePlaylists": UIAction.OPEN_PLAYLISTS,
        "Albums": None,
        "Artists": None,
        "Genres": None,
    },
    "AvailablePlaylists": {
        "PlaylistSelectionList": UIAction.SELECT_PLAYLIST,
    },
    "PlaylistTracks": {
        "PlaylistTracks": UIAction.SELECT_TRACK,
    },
}


def get_action_for_screen_element(screen_name, element_name):
    """
    Return the UIAction for a screen/element pair.

    Returns None when the screen element exists but does not have an
    implemented action yet.
    """
    return SCREEN_ELEMENT_ACTIONS.get(screen_name, {}).get(element_name)
