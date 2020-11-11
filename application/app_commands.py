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
import re
import subprocess
import shlex
import shutil
import webbrowser
from re import Match
from typing import List, Tuple, Optional, Dict
from functools import lru_cache
# from difflib import get_close_matches

# Related third party imports
from pathlib import Path, PosixPath, WindowsPath

# Local application/library specific imports
from .config import verify_app_installed

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


class FindFolderPath(object):
    def __init__(self, folder_name: str) -> None:
        self.folder_name = folder_name

    @lru_cache
    def find_folder_paths(self) -> Optional:
        directories: Dict[str, Optional] = {
            'docs': self.dir_in_documents(),
            'music': self.dir_in_music(),
            'video': self.dir_in_videos(),
            'download': self.dir_in_downloads(),
            'pics': self.dir_in_pictures()
        }

        folder_path: List = []
        for i in directories.values():
            data = i
            if type(data) == list:
                folder_path += data
            continue

        if len(folder_path) == 0:
            return "Folder not found."
        return self.choose_path(folder_path)

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
                return "Invalid input entered"

        chosen: Path = paths_found[0]
        return chosen

    @lru_cache
    def dir_in_documents(self) -> Optional:
        try:
            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(
                f"find ./Documents -iname '{self.folder_name}' -type d "),
                stdout=subprocess.PIPE, universal_newlines=True,
                stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            folders_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                               output.split('\n')]
            return folders_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def dir_in_music(self) -> Optional:
        try:
            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(
                f"find ./Music -iname '{self.folder_name}' -type d "),
                stdout=subprocess.PIPE, universal_newlines=True,
                stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            folders_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                               output.split('\n')]
            return folders_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def dir_in_videos(self) -> Optional:
        try:
            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(
                f"find ./Videos -iname '{self.folder_name}' -type d "),
                stdout=subprocess.PIPE, universal_newlines=True,
                stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            folders_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                               output.split('\n')]
            return folders_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def dir_in_downloads(self) -> Optional:
        try:
            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(
                f"find ./Downloads -iname '{self.folder_name}' -type d "),
                stdout=subprocess.PIPE, universal_newlines=True,
                stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            folders_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                               output.split('\n')]
            return folders_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def dir_in_pictures(self) -> Optional:
        try:
            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(
                f"find ./Pictures -iname '{self.folder_name}' -type d "),
                stdout=subprocess.PIPE, universal_newlines=True,
                stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            folders_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                               output.split('\n')]
            return folders_paths_found

        except FileNotFoundError as error:
            return error.strerror


class FindFilePath(object):
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name

    @lru_cache
    def find_file_paths(self) -> Optional:
        files: Dict[str, Optional] = {
            'docs': self.file_in_documents(),
            'music': self.file_in_music(),
            'video': self.file_in_videos(),
            'download': self.file_in_downloads(),
            'pics': self.file_in_pictures()
        }

        file_path: List = []
        for i in files.values():
            data: List = i
            if type(data) == list:
                file_path += data
            continue

        if len(file_path) == 0:
            return "File not found."
        return self.choose_path(file_path)

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
                return "Invalid input entered"

        chosen: Path = paths_found[0]
        return chosen

    @lru_cache
    def file_in_documents(self) -> Optional:
        try:
            list_commands: List[str] = [
                f"find ./Documents",
                f"\( -iname '*{self.file_name}*.doc*' -or -iname '*{self.file_name}*.zip' -type f \)",
                f"-or \( -iname '*{self.file_name}*.pdf' -or -iname '*{self.file_name}*.txt' -type f \)",
                f"-or \( -iname '*{self.file_name}*.pem' -or -iname '*{self.file_name}*.json' -type f \)",
                f"-or \( -iname '*{self.file_name}*.mp4' -or -iname '*{self.file_name}*.mkv' -type f \)",
                f"-or \( -iname '*{self.file_name}*.mp3' -or -iname '*{self.file_name}*.ogg' -type f \)",
                f"-or \( -iname '*{self.file_name}*.jp*g' -or -iname '*{self.file_name}*.png' -type f \)"
            ]
            command: str = " ".join(list_commands)

            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(command),
                                                             stdout=subprocess.PIPE, universal_newlines=True,
                                                             stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            files_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                             output.split('\n')]
            return files_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def file_in_music(self) -> Optional:
        try:
            list_commands: List[str] = [
                f"find ./Music",
                f"-iname '*{self.file_name}*.mp3'",
                f"-or -iname '*{self.file_name}*.ogg' -type f"
            ]
            command: str = " ".join(list_commands)

            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(command),
                                                             stdout=subprocess.PIPE, universal_newlines=True,
                                                             stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            files_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                             output.split('\n')]
            return files_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def file_in_videos(self) -> Optional:
        try:
            list_commands: List[str] = [
                f"find ./Videos",
                f"\( -iname '*{self.file_name}*.mp4' -or -iname '*{self.file_name}*.mkv' -type f \)",
                f"-or -iname '*{self.file_name}*.avi' -type f"
            ]
            command: str = " ".join(list_commands)

            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(command),
                                                             stdout=subprocess.PIPE, universal_newlines=True,
                                                             stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            files_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                             output.split('\n')]
            return files_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def file_in_downloads(self) -> Optional:
        try:
            list_commands: List[str] = [
                f"find ./Downloads",
                f"\( -iname '*{self.file_name}*.pdf' -or -iname '*{self.file_name}*.zip' -type f \)",
                f"-or \( -iname '*{self.file_name}*.png' -or -iname '*{self.file_name}*.jp*g' -type f \)",
                f"-or \( -iname '*{self.file_name}*.pem' -or -iname '*{self.file_name}*.json' -type f \)",
                f"-or \( -iname '*{self.file_name}*.doc*' -or -iname '*{self.file_name}*.mp4' -type f \)",
                f"-or \( -iname '*{self.file_name}*.mkv' -or -iname '*{self.file_name}*.mp3' -type f \)",
                f"-or \( -iname '*{self.file_name}*.txt' -or -iname '*{self.file_name}*.ogg' -type f \)"
            ]
            command: str = " ".join(list_commands)

            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(command),
                                                             stdout=subprocess.PIPE, universal_newlines=True,
                                                             stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            files_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                             output.split('\n')]
            return files_paths_found

        except FileNotFoundError as error:
            return error.strerror

    @lru_cache
    def file_in_pictures(self) -> Optional:
        try:
            list_commands: List[str] = [
                f"find ./Pictures",
                f"\( -iname '*{self.file_name}*.png' -or -iname '*{self.file_name}*.jp*g' -type f \)",
                f"-or -iname '*{self.file_name}*.webp' -type f"
            ]
            command: str = " ".join(list_commands)

            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(command),
                                                             stdout=subprocess.PIPE, universal_newlines=True,
                                                             stderr=subprocess.PIPE, cwd=basedir.home())

            results: Tuple[str, str] = search.communicate()
            stdout, _ = results
            output: str = stdout.rstrip('\n')
            if not output:
                return []
            files_paths_found: List[Path] = [basedir.home().joinpath(path.replace(" ", "\ ")) for path in
                                             output.split('\n')]
            return files_paths_found

        except FileNotFoundError as error:
            return error.strerror


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
        self.screenshot: str = configuration["SCREENSHOT"]


class OpenFolder(Main):
    def __init__(self, search_keyword: str, folder_name: str) -> None:
        super().__init__(Main.configuration)
        # self.path_current_working_directory: Path = basedir
        self.search_keyword: str = search_keyword
        self.folder_name: str = folder_name

    def run(self) -> Optional[str]:
        find_folder_path = FindFolderPath(self.folder_name).find_folder_paths()
        return self.open_with_ide_or_file_browser(find_folder_path) \
            if type(find_folder_path) is PosixPath or WindowsPath else find_folder_path

    def open_folder_in_ide(self, folder_path: Path) -> str:
        if verify_app_installed(self.ide)[0] is False:
            return f"{self.ide.capitalize()} app not installed"
        try:
            x = subprocess.Popen(shlex.split(f"{self.ide} {folder_path}"),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True, cwd=basedir.home())
            # g, _ = x.communicate()
            return "Done"

        except FileNotFoundError:
            return f"{self.ide.capitalize()} could not open."

    def open_folder_in_file_browser(self, folder_path: Path) -> str:
        if verify_app_installed(self.file_browser)[0] is False:
            return f"{self.file_browser.capitalize()} app not installed"
        try:
            subprocess.Popen(shlex.split(f"{self.file_browser} {folder_path}"),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.file_browser.capitalize()} could not open."

    def open_with_ide_or_file_browser(self, path: Path) -> str:
        # self.path_current_working_directory = path  # Update path for current working directory

        if 'browse folder' in self.search_keyword:
            return self.open_folder_in_file_browser(path)
        elif 'edit folder' in self.search_keyword:
            return self.open_folder_in_ide(path)
        return "Un-supported command."


class OpenApp(Main):
    """
        Some Apps can't open multiple windows of the app at the same time.
    """

    def __init__(self, search_keyword: str) -> None:
        super().__init__(Main.configuration)
        self.search_keyword: str = search_keyword

    @lru_cache
    def launch_app(self) -> str:
        app: str = self.search_keyword
        if (app_name := app.replace("-", "_").upper()) in Main.configuration:
            app = Main.configuration[app_name]

        is_app_installed: Tuple[bool, str] = verify_app_installed(app)
        if is_app_installed[0] is False:
            return f"{app.capitalize()} is not installed."

        try:
            subprocess.Popen(shlex.split(f"{app}"),
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{app.capitalize()} could not open."


class MediaPlayer(Main):
    def __init__(self, media_file_name: str) -> None:
        super().__init__(Main.configuration)
        self.media_file_name: str = media_file_name

    @lru_cache
    def watch_video(self) -> str:
        file_path: Path = FindFilePath(self.media_file_name).find_file_paths()
        if str(file_path).endswith(('.mp4', '.mkv', '.avi')) is False:
            return "Un-supported video file format."

        if type(file_path) is not (PosixPath or WindowsPath):
            return "File not found."

        if self.video_player == "totem":
            try:
                subprocess.Popen(shlex.split(f"{self.video_player} --play {file_path}"),
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                 universal_newlines=True, cwd=basedir.home())
                return "Done"

            except FileNotFoundError:
                return f"{self.video_player} app not installed."
        try:
            subprocess.Popen(shlex.split(f"{self.video_player} {file_path}"),
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.video_player} app not installed."

    @lru_cache
    def play_music(self) -> str:
        file_path: Path = FindFilePath(self.media_file_name).find_file_paths()
        if str(file_path).endswith(('.mp3', '.ogg')) is False:
            return "Un-supported video file format."
        if type(file_path) is not (PosixPath or WindowsPath):
            return "File not found."
        try:
            subprocess.Popen(shlex.split(f"{self.music_player} {file_path}"),
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.music_player} app not installed."


@lru_cache
def totem_commands(command: str):
    list_commands: Dict[str, str] = {
        "play": "--play",
        "pause": "--pause",
        "forward": "--seek-fwd",
        "backward": "--seek-bwd",
        "increase": "--volume-up",
        "decrease": "--volume-down",
        "mute": "--mute",
        "fullscreen": "--fullscreen",
        "quit": "--quit"
    }
    if command not in list_commands.keys():
        return "Un-supported command."
    option: str = list_commands[command]
    try:
        subprocess.Popen(shlex.split(f"totem {option}"),
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                         universal_newlines=True, cwd=basedir.home())
        return "Done"

    except FileNotFoundError:
        return "Videos app not installed."


class SearchOnline(Main):
    def __init__(self, search_term: str) -> None:
        super().__init__(Main.configuration)
        self.keywords: str = search_term

    @lru_cache
    def search(self) -> None:
        url: str = f"https://www.google.com/search?q={self.keywords}"
        browse: webbrowser.BaseBrowser = webbrowser.get(self.web_browser)
        browse.open_new_tab(url)

    @lru_cache
    def locate(self) -> None:
        url: str = f"https://www.google.com/maps/search/{self.keywords}"
        browse: webbrowser.BaseBrowser = webbrowser.get(self.web_browser)
        browse.open_new_tab(url)


class ViewFile(Main):
    def __init__(self, file_name: str) -> None:
        super().__init__(Main.configuration)
        self.file_name: str = file_name

    @lru_cache
    def selector(self) -> str:
        file_path: Path = FindFilePath(self.file_name).find_file_paths()
        if str(file_path).endswith(('.txt', '.json', '.pdf', '.pem')) is False:
            return "Un-supported file format."

        result: Optional[Match[str]] = re.search(r".pdf$", str(file_path), re.IGNORECASE)
        if result:
            return self.open_file_in_pdf_reader(file_path)
        return self.open_file_in_text_editor(file_path)

    @lru_cache
    def open_file_in_text_editor(self, file_path: Path) -> str:
        if verify_app_installed(self.text_editor)[0] is False:
            return f"{self.text_editor.capitalize()} not installed."
        try:
            subprocess.Popen(shlex.split(f"{self.text_editor} {file_path}"),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.text_editor.capitalize()} could not open."

    @lru_cache
    def open_file_in_pdf_reader(self, file_path: Path) -> str:
        if verify_app_installed(self.pdf_reader)[0] is False:
            return f"{self.pdf_reader.capitalize()} not installed."
        try:
            subprocess.Popen(shlex.split(f"{self.pdf_reader} {file_path}"),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.pdf_reader.capitalize()} could not open."


@lru_cache
def open_dir_in_terminal(folder_name: str) -> str:
    folder_path: Path = FindFolderPath(folder_name).find_folder_paths()
    if verify_app_installed("gnome-terminal")[0] is False:
        return f"Gnome Terminal app not installed."
    try:
        subprocess.Popen(shlex.split(f"gnome-terminal --working-directory={folder_path}"),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, cwd=basedir.home())
        return "Done"

    except FileNotFoundError:
        return f"Gnome Terminal could not open."


@lru_cache
def disk_info() -> Tuple[str, str, str]:
    disk_usage = shutil.disk_usage(basedir.home())
    gigabyte: int = 1_000_000_000
    free: float = (disk_usage.free / gigabyte) * 1
    used: float = (disk_usage.used / gigabyte) * 1
    total: float = (disk_usage.total / gigabyte) * 1
    return (f"Free space: {free.__round__(2)}Gb",
            f"Used space: {used.__round__(2)}Gb",
            f"Total space: {total.__round__(2)}Gb")

# Music player -> rhythmbox "`find -iname "*drown*.mp3" -type f`"
# Video player -> totem --play iceblog-2020-08-16_07.09.05.mp4
# Terminal -> gnome-terminal --working-directory="absolute_path"
# PDF READER -> evince ./Downloads/mongodb_document_schema.pdf
