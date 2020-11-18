"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
"""

# Standard library imports
import datetime
from functools import lru_cache
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Union, Callable, Any

# Related third party imports


# Local application/library specific imports
from .app_commands import (OpenFolder, OpenApp, FindFilePath,
                           totem_commands, SearchOnline, open_dir_in_terminal,
                           MediaPlayer, ViewFile, FindFolderPath, BasicCalculator)
from .config import AppInstallationConfig, verify_app_installed


def app_installation() -> str:
    try:
        search_term: str = input("Do you want to configure default apps. [Y]es or [N]o: ").lower()
        if search_term != 'y':
            print(AppInstallationConfig().initial_config())
            return 'default_settings'

        print(AppInstallationConfig("user_settings").initial_config())
        return 'user_settings'
    except ValueError:
        return app_installation()
    except EOFError:
        return ''


def open_folder() -> str:
    try:
        search_term: str = input("Enter search here: ")
        sep: List[str] = search_term.split(" ")
        k, v = " ".join(sep[:2]), " ".join(sep[2:])
        return OpenFolder(search_keyword=k.lower(), folder_name=v).run()
    except EOFError:
        return ''


def version() -> Union[Tuple[bool, str], str]:
    try:
        search_term: str = input("Enter the name of the app you want to verify: ").lower()
        v0: datetime.datetime = datetime.datetime.now()
        finished: Tuple[bool, str] = verify_app_installed(search_term.replace(" ", "-"))
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        return ''


def launch() -> str:
    try:
        search_term: str = input("Enter the name of the app you want to open: ").lower()
        v0: datetime.datetime = datetime.datetime.now()
        finished: str = OpenApp(search_term.replace(" ", "-")).launch_app()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        return ''


def find_file() -> Union[Path, str]:
    try:
        search_term: str = input("Enter the name of the file: ")
        v0: datetime.datetime = datetime.datetime.now()
        finished: Union[Path, str] = FindFilePath(search_term, file_extensions=[".pdf", ".txt", ".zip",
                                                                   ".png", ".jp*g", ".doc*",
                                                                   ".mp4", ".mkv"]).find_file_paths()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        return ''


def find_folder() -> Union[Path, str]:
    try:
        search_term: str = input("Enter the name of the folder: ")
        v0: datetime.datetime = datetime.datetime.now()
        finished: Union[Path, str] = FindFolderPath(search_term).find_folder_paths()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        return ''


def media_player() -> Any:
    try:
        search_term: str = input("Enter media command: ").lower()
        sep: List[str] = search_term.split(" ")
        k, j = sep[0], " ".join(sep[1:])
        if k == "watch" or k == "play":
            media_commands: Dict[str, Any] = {
                "watch": MediaPlayer(j).watch_video,
                "play": MediaPlayer(j).play_music
            }
            v0: datetime.datetime = datetime.datetime.now()
            finished: Any = media_commands.get(k)
            sub: datetime.timedelta = datetime.datetime.now() - v0
            print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
            return finished()
        return "Invalid command"
    except EOFError:
        return ''


def totem_options() -> str:
    try:
        search_term: str = input("Enter option: ").lower()
        option: str = search_term.replace(" ", "_")
        v0: datetime.datetime = datetime.datetime.now()
        finished: str = totem_commands(option)
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        return ''


def browsing() -> str:
    try:
        search_term: str = input("Enter option: ").lower()
        sep: List[str] = search_term.split(" ")
        k, j = sep[0], " ".join(sep[1:])
        if k == "search" or k == "locate":
            browser_commands: Dict[str, Any] = {
                "search": SearchOnline(j).search,
                "locate": SearchOnline(j).locate
            }
            v0: datetime.datetime = datetime.datetime.now()
            finished: Any = browser_commands.get(k)
            finished()
            sub: datetime.timedelta = datetime.datetime.now() - v0
            print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
            return "Done"
        return "Invalid command"
    except EOFError:
        return ''


def terminal_dir() -> str:
    try:
        search_term: str = input("Enter option: ").lower()
        sep: List[str] = search_term.split(" ")
        k, j = " ".join(sep[:3]), " ".join(sep[3:])
        if k == "open terminal in":
            folder_name: str = j.strip()  # strip any whitespace at the beginning and end of text
            v0: datetime.datetime = datetime.datetime.now()
            finished: str = open_dir_in_terminal(folder_name)
            sub: datetime.timedelta = datetime.datetime.now() - v0
            print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
            return finished
        return "Invalid command"
    except EOFError:
        return ''


@lru_cache
def file_viewer() -> str:
    try:
        search_term: str = input("Enter option: ").lower()
        sep: List[str] = search_term.split(" ")
        k, j = " ".join(sep[:2]), " ".join(sep[2:])
        if k == "open file":
            file_name: str = j.strip()
            v0: datetime.datetime = datetime.datetime.now()
            finished: str = ViewFile(file_name).selector()
            sub: datetime.timedelta = datetime.datetime.now() - v0
            print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
            return finished
        return "Invalid command"
    except EOFError:
        return ''


def calculator() -> Union[int, float, str]:
    try:
        search_term: str = input("Enter equation: ")
        finished: Union[int, float, str] = BasicCalculator(search_term).run()
        return finished
    except EOFError:
        return ''
