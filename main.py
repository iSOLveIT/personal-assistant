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
from typing import Dict

# Related third party imports
from pathlib import Path, PurePath
from dotenv import load_dotenv, set_key

# Local application/library specific imports
from application import *
from application.config import AppStartedConfig
from application.app_commands import Main


# Load environment variables from .env file.
env_path: Path = Path('.').resolve().joinpath('configure_files', 'my_pa.env')
if env_path.exists() is False:
    with open(str(env_path), "w") as env_file:
        env_contents: str = f"""# IS_CONFIGURED is 1 if app was configured at installation, 0 otherwise
# SETTINGS shows which settings is used
IS_CONFIGURED="1"
SETTINGS="user_settings"
"""
        env_file.write(env_contents)

load_dotenv(dotenv_path=str(env_path))


def run() -> None:
    get_is_configured: str = str(os.getenv("IS_CONFIGURED"))
    is_configured: bool = bool(int(get_is_configured))
    if is_configured is False:
        settings: str = app_installation()
        set_key(env_path, "IS_CONFIGURED", '1')
        set_key(env_path, "SETTINGS", settings)
        load_dotenv(dotenv_path=str(env_path), override=True)

    configuration: Dict[str, str] = AppStartedConfig().apply_settings()
    Main(configuration)
    print(terminal_dir())


if __name__ == "__main__":
    try:
        print("Press Ctrl-C to terminate while statement")
        while True:
            t0 = dt.now()
            run()
            t1 = dt.now() - t0
            print("App done in {:,.2f} seconds.".format(t1.total_seconds()))
    except KeyboardInterrupt:
        print("\nTerminated")
