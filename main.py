"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports
from datetime import datetime as dt
import os

# Related third party imports
from pathlib import Path
from dotenv import load_dotenv, set_key

# Local application/library specific imports
from application import *
from application.config import AppStartedConfig
from application.app_commands import Main


# Load environment variables from .env file.
env_path = Path('.').resolve().joinpath('configure_files', 'my_pa.env')
load_dotenv(dotenv_path=env_path)


def run() -> None:
    is_configured: bool = bool(int(os.getenv("IS_CONFIGURED")))
    if is_configured is False:
        settings: str = app_installation()
        set_key(env_path, "IS_CONFIGURED", '1')
        set_key(env_path, "SETTINGS", settings)
        load_dotenv(dotenv_path=env_path, override=True)

    configuration: Dict[str, str] = AppStartedConfig().apply_settings()
    Main(configuration)
    print(launch())


if __name__ == "__main__":
    try:
        print("Press Ctrl-C to terminate while statement")
        while True:
            t0 = dt.now()
            run()
            t1 = dt.now() - t0
            print("App done in {:,.2f} seconds.".format(t1.total_seconds()))
            break
    except KeyboardInterrupt:
        print("\nTerminated")
