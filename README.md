# Dead Internet Simulator

A local desktop simulation of an abandoned internet that lives its own life. Explore a dark, mysterious network of forgotten forums, ghost accounts, and digital anomalies.

## Features

- **Autonomous Simulation**: AI-controlled users create threads, post messages, spread rumors, and form relationships without player intervention
- **Dark Atmosphere**: Retro 2000s internet aesthetic with dark theme, monospace fonts, and eerie green accents
- **Mysterious World**: Uncover digital mysteries through exploration of archives, events, and contradictory information
- **Multiple Sections**: Browse sites, forums, users, communities, events, and archives
- **Persistent World**: All simulation state is saved to SQLite database between sessions
- **Player Interaction**: Create your own account, post messages, start threads, and influence the network
- **Configurable Speed**: Adjust simulation speed or pause to observe at your own pace

## Requirements

- Python 3.7+
- Windows (tested on Windows)
- No internet connection required
- Uses only Python standard library (tkinter, sqlite3, threading, etc.)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Run the application

## Running the Application

### On Windows
Double-click `run.bat` or run from command line:
```bash
run.bat
```

### From Command Line
```bash
python main.py
```

## How to Play

1. **Launch**: Start the application - a world will be generated on first run
2. **Explore**: Navigate through tabs (Home, Browser, Forums, Users, Communities, Archive, Events, Settings)
3. **Create Player**: Click "[CREATE/VIEW PLAYER]" in the status bar to join the network
4. **Observe**: Watch as the simulation runs autonomously, creating new content and events
5. **Interact**: Post in forums, create threads, or join communities as your player character
6. **Investigate**: Check the Archive and Events tabs for mysteries to unravel
7. **Control**: Use Settings to pause, adjust speed, or reset the world

## Project Structure

```
dead_internet_simulator/
├── core/           # Configuration and utilities
├── db/             # Database management
├── generators/     # World generation
├── models/         # Data models
├── simulation/     # Autonomous simulation engine
├── ui/             # User interface components
└── app.py          # Main application class
```

## Notes

- The world is procedurally generated on first run
- Mysterious events and connections form over time
- Not all secrets are revealed immediately - explore to uncover them
- The simulation continues even when tabs are not active
- Reset the world from Settings if you want a fresh start

## Warning

This is a simulation of a "dead internet". Expect strange, cryptic, and occasionally unsettling content. The atmosphere is intentionally eerie.

---

*"Something is wrong with the network. It remembers things it shouldn't."*
