"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
"""

# Standard library imports
import datetime
from typing import Optional, Tuple, List

# Related third party imports


# Local application/library specific imports
from .app_commands import (OpenFolder, OpenApp, FindFilePath,
                           totem_commands, SearchOnline, open_dir_in_terminal,
                           MediaPlayer, ViewFile)
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
        pass


def intro() -> Optional[str]:
    try:
        search_term: str = input("Enter search here: ")
        sep: List[str] = search_term.split(" ")
        k, v = " ".join(sep[:2]), " ".join(sep[2:])
        return OpenFolder(search_keyword=k.lower(), folder_name=v).run()
    except EOFError:
        pass


def version() -> Tuple[bool, str]:
    search_term: str = input("Enter the name of the app you want to verify: ")
    # print(search_term, verify_app_installed(search_term).cache_info())
    v0: datetime.datetime = datetime.datetime.now()
    finished: Tuple[bool, str] = verify_app_installed(search_term.replace(" ", "-"))
    sub: datetime.timedelta = datetime.datetime.now() - v0
    print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
    return finished


def launch() -> str:
    try:
        search_term: str = input("Enter the name of the app you want to open: ")
        v0: datetime.datetime = datetime.datetime.now()
        finished: str = OpenApp(search_term.replace(" ", "-")).launch_app()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        pass


def find_file() -> str:
    try:
        search_term: str = input("Enter the name of the file: ")
        v0: datetime.datetime = datetime.datetime.now()
        finished: str = FindFilePath(search_term).find_file_paths()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        pass


def media_player() -> str:
    try:
        search_term: str = input("Enter media command: ").lower()
        sep: List[str] = search_term.split(" ")
        k, j = " ".join(sep[:1]), " ".join(sep[1:])
        if k == "watch":
            v0: datetime.datetime = datetime.datetime.now()
            finished: str = MediaPlayer(j).watch_video()
            sub: datetime.timedelta = datetime.datetime.now() - v0
            print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
            return finished

        v0: datetime.datetime = datetime.datetime.now()
        finished: str = MediaPlayer(j).play_music()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        pass


def totem_options() -> str:
    try:
        search_term: str = input("Enter option: ")
        sep: List[str] = search_term.split(" ")
        k = sep[0]
        v0: datetime.datetime = datetime.datetime.now()
        finished: str = totem_commands(k)
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        pass


def browsing() -> str:
    try:
        search_term: str = input("Enter option: ").lower()
        sep: List[str] = search_term.split(" ")
        k, j = sep[0], " ".join(sep[1:])
        if k == "locate":
            v0: datetime.datetime = datetime.datetime.now()
            SearchOnline(j).locate()
            sub: datetime.timedelta = datetime.datetime.now() - v0
            print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
            return "Done"

        v0: datetime.datetime = datetime.datetime.now()
        SearchOnline(j).search()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return "Done"

    except EOFError:
        pass


def terminal_dir() -> str:
    try:
        search_term: str = input("Enter option: ")
        sep: List[str] = search_term.split(" ")
        k, j = " ".join(sep[:3]), " ".join(sep[3:])
        folder_name: str = j.strip()  # strip any whitespace at the beginning and end of text
        v0: datetime.datetime = datetime.datetime.now()
        finished: str = open_dir_in_terminal(folder_name)
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished
    except EOFError:
        pass


def file_viewer() -> str:
    try:
        search_term: str = input("Enter option: ").lower()
        sep: List[str] = search_term.split(" ")
        k, j = "".join(sep[:2]), " ".join(sep[2:])
        file_name: str = j.strip()
        v0: datetime.datetime = datetime.datetime.now()
        finished: str = ViewFile(file_name).selector()
        sub: datetime.timedelta = datetime.datetime.now() - v0
        print("Function done in {:,.2f} seconds.".format(sub.total_seconds()))
        return finished

    except EOFError:
        pass

# apps = [
#         "vlc", "totem", "twinux", "vlc", "rhythmbox", "twinux", "fromscratch",
#         "evince", "firefox", "totem", "thunderbird", "twinux", "purple-task",
#         "gedit", "nautilus", "gnome-calendar", "code", "knowte", "gimp"
#     ]
