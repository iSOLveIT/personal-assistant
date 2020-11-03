import json
import os
import subprocess
import shlex
from functools import lru_cache
from typing import List, Dict, Tuple, Optional, Type

from pathlib import Path

from .envs import app_default_settings, supported_apps

basedir = Path()


@lru_cache
def verify_app_installed(app_name: str) -> Tuple[bool, str]:
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
    """Base configuration"""

    def __init__(self, settings: Optional[str] = None) -> None:
        if settings is None:
            os.environ.setdefault("SETTINGS", "default_settings")
        else:
            os.environ["SETTINGS"] = settings

    def initial_config(self) -> str:
        if os.getenv("SETTINGS", default="default_settings") == "user_settings":
            return self.initial_user_config()
        else:
            return self.initial_default_config()

    @staticmethod
    @lru_cache
    def initial_default_config() -> str:
        default_config: List[Dict[str, str]] = app_default_settings

        for i in default_config:
            verify_app: Tuple[bool, str] = verify_app_installed(i["value"])
            if verify_app[0] is False:
                print(f"Download {i['value']} for linux")
            continue

        return "Successfully Configured."

    @staticmethod
    @lru_cache
    def initial_user_config() -> str:
        apps_supported: List[Dict[str, Optional[str]]] = supported_apps
        app_allowed_to_change: List[Dict[str, Optional[str]]] = [
            item for item in apps_supported if item["allow_change"] is True]
        apps_default_config: List[Dict[str, str]] = app_default_settings

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
                if verify_app[0] is False:
                    print(f"Download {app} for linux")
                else:
                    i["value"] = app
            continue

        config_dir: Path = basedir.cwd().joinpath("configure_files")
        config_path: Path = config_dir.joinpath("user_settings.json")

        with open(str(config_path), "w") as f:
            json.dump(apps_default_config, f, indent=2)

        return "Successfully Configured."


class AppStartedConfig:
    def apply_settings(self):
        if os.getenv("SETTINGS", default="default_settings") != "user_settings":
            return self.default_settings()

        is_user_settings = self.user_settings()
        if is_user_settings is None:
            print("App needs to be re-configured. Click on the configuration tab.")
            return self.default_settings()
        return is_user_settings

    @staticmethod
    @lru_cache
    def default_settings():
        settings_: List[Dict[str, str]] = app_default_settings

        # Convert the config into a usable Python dictionary object using dictionary comprehension
        config: Dict[str, str] = dict((i["name"], i["value"]) for i in settings_)
        return config

    @staticmethod
    @lru_cache
    def user_settings():
        config_dir = basedir.cwd().joinpath("configure_files")
        config_path: Path = config_dir.joinpath("user_settings.json")
        with open(str(config_path), "r") as f:
            settings_: List[Dict[str, str]] = json.load(f)

        # Convert the config into a usable Python dictionary object using dictionary comprehension
        config: Dict[str, str] = dict((i["name"], i["value"]) for i in settings_)
        return config

# thj = Path().cwd().parent.joinpath("configure_files")
# print(thj)


# Errors
# IndexError: list index out of range
# ValueError: invalid literal for int() with base 10: ''
