from pathlib import Path
import os
import json
from typing import List, Dict

from project.app_commands import VerifyAppCommand, SearchOnline


class Config(object):
    """Base configuration"""
    def __init__(self, settings: str = None) -> None:
        self.config_dir: Path = Path.cwd().joinpath("config")
        if settings is None:
            os.environ.setdefault("settings", "default_settings")
        else:
            os.environ["settings"] = settings

    def chose_settings(self):
        selected_setting = os.environ.get("settings")
        return self.user_config() if selected_setting == "user_settings"\
            else self.default_config()

    def default_config(self):
        config_file_name: str = f"{os.environ.get('settings')}.json"
        config_path: Path = self.config_dir.joinpath(config_file_name)
        with open(config_path, "r") as f:
            config: List = json.load(f)

        for i in config:
            verify_app = VerifyAppCommand(i["value"]).check_app_info()
            if verify_app[0] is False:
                SearchOnline(f"Download {i['value']} for linux")
            continue

        # Convert the config into a usable Python dictionary object using dictionary comprehension
        config: Dict = dict((i["name"], i["value"]) for i in config)
        return config

    def user_config(self):
        config_file_name: str = f"{os.environ.get('settings')}.json"
        config_path: Path = self.config_dir.joinpath(config_file_name)

        supported_apps_path = self.config_dir.joinpath("supported_apps.json")
        with open(supported_apps_path, "r") as f:
            supported_apps: dict = json.load(f)

        app_setting_user_can_select_one = [app for app in supported_apps if app["allow_change"] is True]

        with open(config_path, "r") as f:
            user_config: List = json.load(f)

        user_selected_choices = {}
        for app_setting in app_setting_user_can_select_one:
            print(f"Choose a default {app_setting['name']} app from the menu below")
            [print(f"\t[{int(app_setting['value'].index(choice) + 1)}]: {choice['app_name']}\
             - {choice['description']}") for choice in app_setting["value"]]

            answer: int = int(input("Enter the number assigned to an app in the menu above: "))
            selected_app_name = app_setting["value"][int(answer - 1)]["app_name"]
            user_selected_choices.update([(app_setting["name"], selected_app_name)])

        for i in user_config:
            if (app_name := i["name"]) in user_selected_choices:
                app = user_selected_choices[app_name]
                verify_app = VerifyAppCommand(app).check_app_info()
                if verify_app[0] is False:
                    SearchOnline(f"Download {app} for linux")
                else:
                    i["value"] = app
            continue

        with open(config_path, "w+") as f:
            json.dump(user_config, f, indent=4, sort_keys=True)
            config: List = json.load(f)

        # Convert the config into a usable Python dictionary object using dictionary comprehension
        config: Dict = dict((i["name"], i["value"]) for i in config)
        return config


sd = Config()
print(sd.chose_settings())


