"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports
import datetime
import os
from typing import Dict

# Related third party imports
from pathlib import Path
from dotenv import load_dotenv, set_key

# Local application/library specific imports
from application import intro, app_installation
from application.config import AppStartedConfig
from application.app_commands import Main


env_path = Path('.').resolve().joinpath('configure_files', 'my_pa.env')
load_dotenv(dotenv_path=env_path)


def run():
    t0 = datetime.datetime.now()
    is_configured = bool(int(os.getenv("IS_CONFIGURED")))
    print(is_configured)
    if is_configured is False:
        settings = app_installation()
        set_key(env_path, "IS_CONFIGURED", '1')
        set_key(env_path, "SETTINGS", settings)
        load_dotenv(dotenv_path=env_path, override=True)

    configuration: Dict[str, str] = AppStartedConfig().apply_settings()
    Main(configuration)
    print(intro())
    dt = datetime.datetime.now() - t0
    print("Synchronous version done in {:,.2f} seconds.".format(dt.total_seconds()))


if __name__ == "__main__":
    while True:
        run()
