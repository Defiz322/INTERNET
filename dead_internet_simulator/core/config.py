"""
Configuration and constants for Dead Internet Simulator
"""
import os
from pathlib import Path

# Base paths
APP_DIR = Path(__file__).parent.parent.parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "dead_internet.db"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Simulation settings
DEFAULT_SIM_SPEED = 1.0  # 1.0 = real-time, higher = faster
MIN_SIM_SPEED = 0.1
MAX_SIM_SPEED = 10.0

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 1000
MIN_WINDOW_HEIGHT = 700

# Theme colors - dark abandoned internet aesthetic
COLORS = {
    "bg_primary": "#0a0a0a",
    "bg_secondary": "#111111",
    "bg_tertiary": "#1a1a1a",
    "bg_hover": "#252525",
    "border": "#333333",
    "text_primary": "#cccccc",
    "text_secondary": "#888888",
    "text_accent": "#00ff88",
    "text_warning": "#ffaa00",
    "text_danger": "#ff4444",
    "text_link": "#00ccff",
    "green_dim": "#004422",
    "green_bright": "#00ff88",
}

# Fonts
FONT_MONO = ("Consolas", 9)
FONT_MONO_SMALL = ("Consolas", 8)
FONT_MONO_LARGE = ("Consolas", 11)
FONT_TITLE = ("Consolas", 12, "bold")

# Character traits
TRAITS = [
    "paranoid", "curious", "aggressive", "passive", "skeptical",
    "gullible", "secretive", "outspoken", "lonely", "obsessive",
    "nostalgic", "conspiratorial", "technical", "artistic", "mysterious"
]

# Interests
INTERESTS = [
    "old web", "forum drama", "conspiracy theories", "retro tech",
    "digital archaeology", "net art", "ghost stories", "weird sites",
    "cryptic messages", "lost media", "hacking history", "vaporwave",
    "cyber folklore", "abandoned projects", "data corruption"
]

# Site types
SITE_TYPES = [
    "forum", "blog", "imageboard", "wiki", "personal page",
    "archive", "chatlog", "directory", "cryptic page"
]
