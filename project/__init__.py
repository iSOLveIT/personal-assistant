"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports


# Related third party imports


# Local application/library specific imports
from .app_commands import OpenFolder, VerifyAppCommand


class App:
    @staticmethod
    def intro():
        search_term = input("Enter the name of the folder you want to open: ")
        return OpenFolder(search_term, app='code').find_folder_paths()

    @staticmethod
    def version():
        search_term = input("Enter the name of the app you want to verify: ")
        return VerifyAppCommand(search_term).check_app_info()


message = App()
