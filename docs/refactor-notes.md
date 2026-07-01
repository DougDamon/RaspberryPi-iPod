# RaspberryPi-iPod Refactor Plan

## Project Context

This is an open-source Raspberry Pi Zero 2 W portable media player project with:

- 2-inch display
- Rotary encoder
- Four display buttons
- Existing working hardware prototype
- Current working software prototype
- Current goal: refactor before adding major new features

The current main entry point is:

- `piPod.py`

Most current application modules live under:

- `common/`

Including:

- `common/pipodgui.py`
- `common/pipodgui_navigation.py`
- `common/pipodaudio.py`
- `common/musicdatabase.py`
- `common/rotaryencoder.py`
- `common/pipodconfiguration.py`

## Refactor Philosophy

Refactor in very small sessions.

Each session should:

- Have one clear goal
- Leave the app runnable
- Avoid behavior changes unless intentional
- End with a Git commit
- Be testable on the Raspberry Pi hardware

Do not do a large rewrite.

## Git Workflow

Use a dedicated branch:

```bash
git checkout refactor

main should remain the known-good prototype.

refactor is where architecture cleanup happens.

 ****  Overall Roadmap  ****
Session 1 — Documentation structure

Done.

Created:

docs/architecture.md
docs/roadmap.md

No code moved.

Session 2 — Create package folders under common

Goal: prepare the future structure without moving code yet.

Create empty folders:
common/
    audio/
    config/
    input/
    library/
    ui/

Each should contain:
__init__.py

No existing Python files should be moved yet.
No existing Python files should be moved yet.

Commit message suggestion: git commit -m "Create package structure under common"

Session 3 — Move configuration

Move: common/pipodconfiguration.py
to: common/config/settings.py

Then update imports only as needed.

Test on the Pi.

Commit.

Session 4 — Move rotary encoder input

Move: common/rotaryencoder.py
to: common/input/rotary.py

Update imports.
Test.
Commit.

Session 5 — Move audio module

Move: common/pipodaudio.py
to: common/audio/player.py

Do not replace pygame yet.

Only move/wrap current behavior.

Test.
Commit.

Session 6 — Move music database

Move: common/musicdatabase.py
to: common/library/database.py

Update imports.
Test.
Commit.

Session 7 — UI cleanup begins

Start splitting responsibilities from:

common/pipodgui.py
common/pipodgui_navigation.py

Potential future locations:

common/ui/
    screen_manager.py
    theme.py
    widgets.py
    screens/

Do this slowly, one piece at a time.

Future Feature Goals

After the architecture is stable:

Support FLAC/OGG/M4A/AAC/etc.
Replace pygame audio backend, likely with VLC or another backend
Add library scanning/imports
Detect new audio files from folder structure
Read and enrich tag metadata
Support non-music audio:
audiobooks
Old Time Radio
podcasts
Add configurable button mappings
Improve playlist/library management
Add search, favorites, queue, themes, resume playback, bookmarks, and sleep timer
Important Rule

Do not start enhancing features until the current functionality is refactored into a cleaner architecture.

For **Session 2**, yes: just create the empty folders and `__init__.py` files. No code movement yet.
