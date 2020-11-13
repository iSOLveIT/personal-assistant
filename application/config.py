"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports
import json
import os
import subprocess
import shlex
from functools import lru_cache
from typing import List, Dict, Tuple, Optional

# Related third party imports
from pathlib import Path

# Local application/library specific imports
from .envs import app_default_settings, supported_apps

basedir = Path()    # Represents a filesystem path depending on your system.


@lru_cache
def verify_app_installed(app_name: str) -> Tuple[bool, str]:
    """
    Function for running bash commands to verify if an app is installed.

    :param app_name: Sets name of the application to verify.
    :returns: (Boolean, "Type of Application") or (Boolean, "Not Found")
    """
    try:
        app_check: subprocess.Popen[str] = subprocess.Popen(shlex.split(f"dpkg -s {app_name}"),
                                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                            universal_newlines=True, cwd=basedir.home())
        std_out, std_error = app_check.communicate()

        if std_error:
            snap_check: subprocess.Popen[str] = subprocess.Popen(shlex.split(f"snap list | grep '{app_name}'"),
                                                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                                 universal_newlines=True, cwd=basedir.home())
            snap_std_out, snap_std_error = snap_check.communicate()
            return (True, "Snap Application") if snap_std_out else (False, "Not Found")

        return True, "Debian Application"

    except FileNotFoundError:
        return False, "Not Found"


class AppInstallationConfig(object):
    """
    Contains functions for configuring apps to use for better software performance.
    """

    def __init__(self, settings: Optional[str] = None) -> None:
        """
        Initializes Class.

        :param settings: Value to be used for the SETTINGS environment variable.
        """
        if settings is None:
            os.environ.setdefault("SETTINGS", "default_settings")
        else:
            os.environ["SETTINGS"] = settings

    def initial_config(self) -> str:
        """
        Function for selecting which configuration method to use.

        :return: Configuration method.
        """
        if os.getenv("SETTINGS", default="default_settings") == "user_settings":
            return self.initial_user_config()
        else:
            return self.initial_default_config()

    @staticmethod
    @lru_cache
    def initial_default_config() -> str:
        """
        Function for configuring software to use the default settings.

        :return: Successfully Configured.
        """
        default_config: List[Dict[str, str]] = app_default_settings

        for i in default_config:
            verify_app: Tuple[bool, str] = verify_app_installed(i["value"])
            if verify_app[0] is True:
                # TODO: Put all apps not installed in a list and show it to user in readable form
                continue
        return "Successfully Configured."

    @staticmethod
    @lru_cache
    def initial_user_config() -> str:
        """
        Function for configuring software to use the user settings and store the settings in a file.

        :return: Successfully Configured.
        """
        apps_supported: List[Dict[str, Optional[str]]] = supported_apps     # Apps supported by software.
        app_allowed_to_change: List[Dict[str, Optional[str]]] = [
            item for item in apps_supported if item["allow_change"] is True]    # Supported apps user can change.
        apps_default_config: List[Dict[str, str]] = app_default_settings    # Default settings

        user_selected_choices: Dict[str, str] = {}
        for app_setting in app_allowed_to_change:
            print(f"Choose a default {app_setting['name']} app from the menu below")
            for choice in app_setting["value"]:
                print(f"\t[{int(app_setting['value'].index(choice) + 1)}]: {choice.get('app_name')}",
                      f"\t - {choice.get('description')}")

            try:
                answer: int = int(input("Enter the number assigned to an app in the menu above: "))
                selected_app_name: Optional[str] = app_setting["value"][int(answer - 1)].get("app_name")
            except (ValueError, IndexError):
                print("Invalid input or Nothing entered")
                selected_app_name = None

            user_selected_choices[app_setting["name"]] = selected_app_name

        for i in apps_default_config:
            if (app_name := i["name"]) in user_selected_choices:
                app: str = user_selected_choices[app_name]
                if app is None:
                    continue

                verify_app: Tuple[bool, str] = verify_app_installed(app)
                if verify_app[0] is True:
                    # TODO: Put all apps not installed in a list and show it to user in readable form
                    i["value"] = app
            continue

        config_dir: Path = basedir.cwd().joinpath("configure_files")
        config_path: Path = config_dir.joinpath("user_settings.json")

        with open(str(config_path), "w") as f:
            # Store user settings in JSON file
            json.dump(apps_default_config, f, indent=2)

        return "Successfully Configured."


class AppStartedConfig:
    """
    Contains functions for applying software settings at runtime.
    """
    def apply_settings(self) -> Dict[str, str]:
        """
        Function for selecting which settings method to apply at runtime.

        :return: Settings (dict).
        """
        if os.getenv("SETTINGS", default="default_settings") != "user_settings":
            return self.default_settings()

        is_user_settings: Optional[Dict[str, str]] = self.user_settings()
        if is_user_settings is None:
            print("App needs to be re-configured. Click on the configuration tab.")
            return self.default_settings()
        return is_user_settings

    @staticmethod
    @lru_cache
    def default_settings() -> Dict[str, str]:
        """
        Function for converting :settings_: list into a dictionary object.

        :return: Dict object.
        """
        settings_: List[Dict[str, str]] = app_default_settings

        # Convert the config into a usable Python dictionary object using dictionary comprehension
        config: Dict[str, str] = dict((i["name"], i["value"]) for i in settings_)
        return config

    @staticmethod
    @lru_cache
    def user_settings() -> Optional[Dict[str, str]]:
        """
        Function for converting :settings_: list into a dictionary object.

        :return: Dict object.
        """
        config_dir: Path = basedir.cwd().joinpath("configure_files")
        config_path: Path = config_dir.joinpath("user_settings.json")
        with open(str(config_path), "r") as f:
            # Load user settings from settings JSON file.
            settings_: List[Dict[str, str]] = json.load(f)

        # Convert the config into a usable Python dictionary object using dictionary comprehension
        config: Dict[str, str] = dict((i["name"], i["value"]) for i in settings_)
        return config


# Errors
# IndexError: list index out of range
# ValueError: invalid literal for int() with base 10: ''
