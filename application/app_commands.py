"""
    Author: Duodu Randy
    Project: Personal Assistant
    Description: A speech and text recognition program for experimental purposes.
    Date Created: Tuesday, 6th October, 2020
    Tech Stacks: Python
    Topics Learnt: Git
"""

# Standard library imports
# import os
import subprocess
import shlex
from typing import List, Tuple, AnyStr, Optional, Dict

# Related third party imports
from pathlib import Path, PosixPath

# Local application/library specific imports
from .config import VerifyAppCommand, AppStartedConfig

basedir = Path()


# bashCom = str("ps aux | awk '{ for(i=1;i<=NF;i++) {if ( i >= 11 ) printf $i' '}; printf '\n' }' | grep code | grep personal_assistant")
# bashCom = f"ps axu"
# # bashCom = f"ls -ll"
# process = subprocess.Popen(shlex.split(bashCom),
# stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#
#
# working_trees = []
# for output in process.stdout.readlines():
#     project_name = 'personal_assistant'
#     if ('code' and project_name) in output:
#         sd = output.split("/home")[-1]
#         working_trees.append(f"/home{sd}".strip('\n'))
#
# print(f"Output: {working_trees}")
#
# msg = "testing app"
# # Git Add (Stage Files) and Git Commit(Commit Files)
# for working_tree in working_trees:
#     subprocess.Popen(shlex.split("git add ."),
#     stdout=subprocess.PIPE,universal_newlines=True,
#     cwd=working_tree)
#
#     process_two = subprocess.Popen(shlex.split(f"git commit -m {msg.replace(' ', '_')}"),
#     stdout=subprocess.PIPE,universal_newlines=True,
#     cwd=working_tree, stderr=subprocess.PIPE)
#
#     output, error = process_two.communicate()
#     print('Git info: ', output)
#     print(str(error.capitalize()))


class FindFolder(object):
    def __init__(self, folder_name: str) -> None:
        self.folder_name = folder_name

    def find_folder_paths(self) -> Optional:
        try:
            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(f"find -iname '{self.folder_name}' -type d "),
                                                             stdout=subprocess.PIPE, universal_newlines=True,
                                                             stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return f"'{self.folder_name}' folder does not exist"
            folders_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                               output.split('\n')]
            return self.choose_path(folders_paths_found)

        except FileNotFoundError as error:
            return error.strerror

    @staticmethod
    def choose_path(paths_found: List[Path]) -> Optional:
        if (len(paths_found)) > 1:
            choices: List[Tuple[int, Path]] = [(int(paths_found.index(path)), path) for path in paths_found]
            print("Select the correct path you want from the menu below.")
            [print(f"\t[{choice[0] + 1}] - {choice[1]}") for choice in choices]
            try:
                answer: int = int(input("Enter the number for the correct path from the menu above: "))
                selected_path: Path = choices[int(answer - 1)][1]
                return selected_path

            except (ValueError, IndexError):
                return "Invalid input or Nothing entered"

        chosen: Path = paths_found[0]
        return chosen


class Main(object):
    configuration: Dict[str, str] = {}

    def __init__(self, configuration: Dict[str, str]) -> None:
        Main.configuration = configuration
        self.ide: str = configuration["IDE"]
        self.file_browser: str = configuration["FOLDER_BROWSER"]
        self.video_player: str = configuration["VIDEO_PLAYER"]
        self.music_player: str = configuration["MUSIC_PLAYER"]
        self.text_editor: str = configuration["TEXT_EDITOR"]
        self.web_browser: str = configuration["WEB_BROWSER"]
        self.terminal: str = configuration["TERMINAL"]
        self.mail_client: str = configuration["MAIL_CLIENT"]
        self.calendar: str = configuration["CALENDAR"]
        self.calculator: str = configuration["CALCULATOR"]
        self.pdf_reader: str = configuration["PDF_READER"]
        self.screenshot: str = configuration["SCREENSHOT_APP"]


class OpenFolder(Main):
    def __init__(self, search_keyword: str, folder_name: str) -> None:
        super().__init__(Main.configuration)
        self.path_current_working_directory: Path = basedir
        self.search_keyword: str = search_keyword
        self.folder_name: str = folder_name

    def run(self) -> Optional[str]:
        find_folder_path = FindFolder(self.folder_name).find_folder_paths()
        return self.open_with_ide_or_file_browser(find_folder_path) \
            if type(find_folder_path) is PosixPath else find_folder_path

    def open_folder_in_ide(self, folder_path: Path) -> str:
        print("IDE", self.ide)
        if VerifyAppCommand(self.ide).check_app_info()[0] is False:
            return f"{self.ide.capitalize()} not installed"
        try:
            x = subprocess.Popen(shlex.split(f"{self.ide} {folder_path}"),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True, cwd=basedir.home())
            # g, _ = x.communicate()
            return "Done"

        except FileNotFoundError as error:
            return error.strerror

    def open_folder_in_file_browser(self, folder_path: Path) -> str:
        if VerifyAppCommand(self.file_browser).check_app_info()[0] is False:
            return f"{self.file_browser.capitalize()} not installed"
        try:
            subprocess.Popen(shlex.split(f"{self.file_browser} {folder_path}"),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError as error:
            return error.strerror

    def open_with_ide_or_file_browser(self, path: Path) -> str:
        self.path_current_working_directory = path  # Update path for current working directory

        if 'browse folder' in self.search_keyword:
            return self.open_folder_in_file_browser(path)
        elif 'edit folder' in self.search_keyword:
            return self.open_folder_in_ide(path)
        return "Folder couldn't be opened."


# class OpenVideoFile(Main):
#     def __init__(self) -> None:
#         super().__init__()
#         # find -iname "*mulan*.mp4" -or -iname "*mulan*.mkv" -type f


class SearchOnline(Main):
    def __init__(self, search_term: str) -> None:
        super().__init__(Main.configuration)


class OpenApp(Main):
    """
        Can't open multiple windows of an app at the same time.
    """

    def __init__(self, search_keyword: str) -> None:
        super().__init__(Main.configuration)
        self.search_keyword: str = search_keyword

    def launch_app(self):
        app = self.search_keyword
        if (app_name := app.upper()) in Main.configuration:
            app = Main.configuration[app_name]

        is_app_installed: Tuple[bool, str] = VerifyAppCommand(app).check_app_info()
        if is_app_installed[0] is False:
            return f"{app.capitalize()} not installed"

        if is_app_installed[1] == "Snap Application":
            try:
                subprocess.Popen(shlex.split(f"{app}"),
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                 universal_newlines=True, cwd=basedir.home())

                return "Done"
            except FileNotFoundError as error:
                return error.strerror

        try:
            subprocess.Popen(shlex.split(f"{app}"), universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError as error:
            return error.strerror

# def open_folder_in_pycharm(search_term) -> Tuple:
#     folder = basedir.home().joinpath("Codes")
#     try:
#         x = subprocess.Popen(shlex.split(f"find -iname *{search_term}* -type f"), stdout=subprocess.PIPE,
#                              stderr=subprocess.PIPE, universal_newlines=True, cwd=basedir.home())
#         g, q = x.communicate()
#         return g, q
#
#     except FileNotFoundError as error:
#         return error.strerror

# Music player -> rhythmbox "`find -iname "*drown*.mp3" -type f`"
# Video player -> totem --play iceblog-2020-08-16_07.09.05.mp4
# Terminal -> gnome-terminal --working-directory="absolute_path"


# s = input("Enter file: ")
# print(open_folder_in_pycharm(s))
