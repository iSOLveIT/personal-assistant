"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
"""

# Standard library imports
from typing import Optional, Tuple, Dict
import os

# Related third party imports


# Local application/library specific imports
from .app_commands import OpenFolder, OpenApp, Main
from .config import VerifyAppCommand, AppInstallationConfig, AppStartedConfig


def app_installation():
    try:
        search_term = input("Do you want to configure default apps. [Y]es or [N]o: ").lower()
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
        search_term = input("Enter search here: ")
        sep = search_term.split(" ")
        k, v = " ".join(sep[:2]), " ".join(sep[2:])
        return OpenFolder(search_keyword=k.lower(), folder_name=v).run()
    except EOFError:
        pass


def version() -> Tuple[bool, str]:
    search_term = input("Enter the name of the app you want to verify: ")
    return VerifyAppCommand(search_term).check_app_info()


def launch():
    try:
        search_term = input("Enter the name of the app you want to open: ")
        return OpenApp(search_term).launch_app()
    except EOFError:
        pass
