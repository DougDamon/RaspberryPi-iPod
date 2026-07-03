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

These controls should work consistently from anywhere in the interface:

| Control | Action |
|---|---|
| Side Volume Down | Decrease volume |
| Side Volume Up | Increase volume |

Volume should not require looking at the screen and should be handled globally by the application, not by individual screens.

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
