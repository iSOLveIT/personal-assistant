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
from pathlib import Path
import subprocess
import shlex
from typing import List, Tuple, AnyStr, Optional

# Related third party imports


# Local application/library specific imports


home = Path.home()


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
class Main(object):
    def __init__(self, editor: str = None, file_browser: str = None, video_player: str = None) -> None:
        self.path_home_directory: Path = Path.home()
        self.editor: str = editor
        self.file_browser: str = file_browser
        self.video_player: str = video_player


class OpenFolder(Main):
    def __init__(self, search_term: str, app: str = None) -> None:
        super().__init__(self.editor, self.file_browser, self.video_player)
        self.path_current_working_directory: str = ""
        self.search_term: str = search_term
        self.app: str = app

    def find_folder_paths(self) -> Optional:
        try:
            search: subprocess.Popen = subprocess.Popen(shlex.split(f"find -type d -iname {self.search_term}"),
                                                        stdout=subprocess.PIPE, universal_newlines=True,
                                                        stderr=subprocess.PIPE, cwd=self.path_home_directory)

            results: Tuple[AnyStr, AnyStr] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if len(output) == 0:
                return f"No folder with the name {self.search_term} exist"
            folders_found_paths: List[Path] = [self.path_home_directory.joinpath(path.replace(" ", "\ ")) for path in
                                               output.split('\n')]
            return self.choose_correct_path(folders_found_paths)

        except FileNotFoundError as error:
            return error.strerror

    def choose_correct_path(self, paths_found: List[Path]) -> str:
        if (len(paths_found)) > 1:
            choices: List[Tuple[int, Path]] = [(int(paths_found.index(path)), path) for path in paths_found]
            print("Select the correct path you want from the menu below.")
            [print(f"\t[{choice[0] + 1}] - {choice[1]}") for choice in choices]
            answer: int = int(input("Enter the number for the correct path from the menu above: "))
            _, selected_path = choices[int(answer - 1)]
            self.path_current_working_directory = selected_path  # Update path for current working directory
            return self.open_with_code_or_nautilus(selected_path)

        chosen: Path = paths_found[0]
        self.path_current_working_directory = chosen  # Update path for current working directory
        return self.open_with_code_or_nautilus(chosen)

    def open_with_code_or_nautilus(self, path: Path) -> str:
        app = self.app
        if app is None or 'file browser' in app or 'file manager' in app:
            return self.open_folder_in_nautilus(path)
        elif 'vscode' in app or 'code' in app:
            return self.open_folder_in_code(path)
        else:
            apps = {
                'v': self.open_folder_in_code,
                'f': self.open_folder_in_nautilus,
            }

            answer: str = input("Choose app to open with. [V]sCode or [F]ile Browser: ").lower()
            menu = apps.get(answer)
            return "Folder couldn't be opened." if menu is None else menu(path)

    def open_folder_in_code(self, folder_path: Path) -> str:
        if VerifyAppCommand(self.editor).check_app_info() is False:
            return "VSCode not installed"
        try:
            subprocess.Popen(shlex.split(f"{self.editor} {folder_path}"),
                             universal_newlines=True, cwd=self.path_home_directory)
            return "Done"

        except FileNotFoundError as error:
            return error.strerror

    def open_folder_in_pycharm(self, folder_path: Path) -> str:
        # if VerifyCommand(self.editor).check_version() is False:
        #     return "PyCharm Community not installed"
        try:
            x = subprocess.Popen(shlex.split(f"pycharm-community {folder_path}"), stdout=subprocess.PIPE,
                                 universal_newlines=True, cwd=self.path_home_directory)
            g, _ = x.communicate()
            return "Done"

        except FileNotFoundError as error:
            return error.strerror

    def open_folder_in_nautilus(self, folder_path: Path) -> str:
        if VerifyAppCommand(self.editor).check_app_info() is False:
            return "Nautilus file manager not installed"
        try:
            subprocess.Popen(shlex.split(f"{self.file_browser} {folder_path}"),
                             universal_newlines=True, cwd=self.path_home_directory)
            return "Done"

        except FileNotFoundError as error:
            return error.strerror


class OpenVideoFile(Main):
    def __init__(self) -> None:
        super().__init__()
        # find -iname "*mulan*.mp4" -or -iname "*mulan*.mkv" -type f


class VerifyAppCommand(Main):
    def __init__(self, command: str) -> None:
        super().__init__()
        self.command = command

    def check_app_info(self) -> Tuple[bool, str]:
        snap_check: subprocess.Popen = subprocess.Popen(shlex.split(f"snap info {self.command}"),
                                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                        universal_newlines=True, cwd=self.path_home_directory)

        results: Tuple[AnyStr, AnyStr] = snap_check.communicate()
        std_out, std_error = results
        snap_error: str = std_error.rstrip('\n')

        if snap_error:
            try:
                app_check: subprocess.Popen = subprocess.Popen(shlex.split(f"{self.command} --version"),
                                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                               universal_newlines=True, cwd=self.path_home_directory)

                results: Tuple[AnyStr, AnyStr] = app_check.communicate()
                std_out, std_error = results
                app_output: str = std_out.rstrip('\n')

                if app_output:
                    return True, "Debian Application"

            except FileNotFoundError:
                return False, "Not Found"

        return True, "Snap Application"


def open_folder_in_pycharm() -> str:
    # if VerifyCommand(self.editor).check_version() is False:
    #     return "PyCharm Community not installed"
    folder = home.joinpath("Codes")
    try:
        subprocess.Popen(shlex.split(f"rhythmbox '/home/isolveit/Music/Gospels/Lecrae ft. John Legend - Drown.mp3'"),
                             stdout=subprocess.PIPE, universal_newlines=True, cwd=home)
        # g, _ = x.communicate()
        return "Done"

    except FileNotFoundError as error:
        return error.strerror


class SearchOnline(Main):
    def __init__(self, search_term: str) -> None:
        super().__init__()


if __name__ == "__main__":
    print(open_folder_in_pycharm())


# Music player -> rhythmbox "`find -iname "*drown*.mp3" -type f`"
# Video player -> totem --play iceblog-2020-08-16_07.09.05.mp4