# UI Architecture

## Core UI Goal

The player should be usable with minimal screen attention.

Common playback actions should be available through physical controls, and getting to a preferred playlist should require as few steps as possible.

## Design Principles

- Prefer tactile controls over screen interaction.
- Avoid deep menu navigation for common actions.
- Keep volume controls available through physical buttons.
- Make the Now Playing screen the primary operating mode.
- Keep navigation predictable and reversible.
- Prefer simple, stable behavior over feature density.

## Primary Workflow

The ideal primary workflow is:

1. Power on the device.
2. Start or resume a preferred playlist quickly.
3. Use tactile controls for play/pause, volume, next, previous, and navigation.
4. Minimize the need to look at the screen once playback has started.

## Control Mapping Goals

### Global Controls

- Volume Control
	+ Dedicated side volume buttons are the preferred volume-control method.
	+ Volume Up and Volume Down should work globally from anywhere in the interface. They should not require navigating to a volume control, selecting a volume widget, or looking at the screen.
	+ The existing rotary-accessible volume behavior may remain during early refactoring as a fallback, but it should not be required for normal use.

### Front Controls

The front controls can vary by screen, but should remain predictable.

Possible default mapping:

| Control | Default Action |
|---|---|
| Rotary wheel | Navigate list / change selection |
| Rotary press | Select / Play-Pause on Now Playing |
| PiTFT Button 1 | Back |
| PiTFT Button 2 | Home / Now Playing |
| PiTFT Button 3 | Previous |
| PiTFT Button 4 | Next |

## Future UI Cleanup Questions

- Decide whether rotary-accessible volume control should remain once side volume buttons are implemented.
- Decide whether volume changes should display a temporary on-screen overlay.
- Decide whether volume buttons should work while the display is dimmed or off.