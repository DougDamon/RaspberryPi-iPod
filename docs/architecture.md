# Current Architecture

main.py
    |
    +-- GUI
    |     |
    |     +-- Audio
    |     +-- Database
    |     +-- Navigation
    |
    +-- Rotary Encoder
    |
    +-- Configuration

Current Problems

- GUI owns too much state
- Audio tightly coupled to GUI
- Playlist logic mixed with UI
- Global state
