# Standard library imports
from typing import List, Dict, Optional


app_default_settings: List[Dict[str, str]] = [
    {
        "name": "MUSIC_PLAYER",
        "value": "rhythmbox"
    },
    {
        "name": "VIDEO_PLAYER",
        "value": "totem"
    },
    {
        "name": "FOLDER_BROWSER",
        "value": "nautilus"
    },
    {
        "name": "TEXT_EDITOR",
        "value": "gedit"
    },
    {
        "name": "IDE",
        "value": "code"
    },
    {
        "name": "WEB_BROWSER",
        "value": "firefox"
    },
    {
        "name": "TERMINAL",
        "value": "gnome-terminal"
    },
    {
        "name": "MAIL_CLIENT",
        "value": "thunderbird"
    },
    {
        "name": "CALENDAR",
        "value": "gnome-calendar"
    },
    {
        "name": "CALCULATOR",
        "value": "gnome-calculator"
    },
    {
        "name": "PDF_READER",
        "value": "evince"
    },
    {
        "name": "SCREENSHOT",
        "value": "gnome-screenshot"
    }
]

supported_apps: List[Dict[str, Optional[str]]] = [
    {
        "name": "MUSIC_PLAYER",
        "value": [
          {"app_name": "rhythmbox", "description": "Pre-installed music player"}
        ],
        "allow_change": False
    },
    {
        "name": "VIDEO_PLAYER",
        "value": [
          {"app_name": "totem", "description": "Pre-installed video player"},
          {"app_name": "vlc", "description": "VLC media player"}
        ],
        "allow_change": True
    },
    {
        "name": "FOLDER_BROWSER",
        "value": [
          {"app_name": "nautilus", "description": "Pre-installed file manager"}
        ],
        "allow_change": False
    },
    {
        "name": "TEXT_EDITOR",
        "value": [
          {"app_name": "gedit", "description": "Pre-installed graphical text editor"},
          {"app_name": "code", "description": "Visual Studio Code IDE by Microsoft"}
        ],
        "allow_change": True
    },
    {
        "name": "IDE",
        "value": [
          {"app_name": "code", "description": "Visual Studio Code IDE by Microsoft"},
          {"app_name": "pycharm-community", "description": "PyCharm IDE by JetBrains"}
        ],
        "allow_change": True
    },
    {
        "name": "WEB_BROWSER",
        "value": [
          {"app_name": "firefox", "description": "Pre-installed web browser by Mozilla"},
          {"app_name": "google-chrome", "description": "Google Chrome web browser by Google"},
          {"app_name": "opera", "description": "Opera web browser by Opera Software"}
        ],
        "allow_change": True
    },
    {
        "name": "TERMINAL",
        "value": [
          {"app_name": "gnome-terminal", "description": "Pre-install bash terminal"}
        ],
        "allow_change": False
    },
    {
        "name": "MAIL_CLIENT",
        "value": [
          {"app_name": "thunderbird", "description": "Pre-installed GUI mail client by Mozilla"}
        ],
        "allow_change": False
    },
    {
        "name": "CALENDAR",
        "value": [
          {"app_name": "gnome-calendar", "description": "Pre-installed GNOME calendar"}
        ],
        "allow_change": False
    },
    {
        "name": "CALCULATOR",
        "value": [
          {"app_name": "gnome-calculator", "description": "Pre-installed GNOME calculator"}
        ],
        "allow_change": False
    },
    {
        "name": "PDF_READER",
        "value": [
          {"app_name": "evince", "description": "Pre-installed PDF document viewer"}
        ],
        "allow_change": False
    },
    {
        "name": "SCREENSHOT_APP",
        "value": [
          {"app_name": "gnome-screenshot", "description": "Pre-installed GNOME screenshot app"}
        ],
        "allow_change": False
    }
]
