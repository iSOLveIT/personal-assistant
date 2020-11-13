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


basedir = Path()    # Represents a filesystem path depending on your system.


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
    """
    Contains functions for finding folder paths.
    """
    def __init__(self, folder_name: str) -> None:
        """
        Initializes Class.

        :param folder_name: Sets name of folder.
        """
        self.folder_name: str = folder_name
        self.folder_path: List[Path] = []

    @lru_cache
    def find_folder_paths(self) -> Optional:
        """
        Function for finding directory paths that matches the specified folder name.

        :return: Folder path or Error message.
        """
        directories: List[str] = ["Documents", "Music",
                                  "Videos", "Downloads", "Pictures"]

        folder_path: List = []
        # Execute a for loop based on the total elements in the :directories: list,
        # then assign each element to the :self.folders_in_home_dir: method.
        for i in directories:
            data: List[Path] = self.folders_in_home_dir(i)
            if type(data) == list:
                folder_path += data
            continue

        if len(folder_path) == 0:
            return "Folder does not exist."
        self.folder_path = folder_path
        return self.choose_path()

    @lru_cache
    def choose_path(self) -> Optional:
        """
        Function for choosing the preferred path that matches a folder name, if software finds more than one match.

        :return: Error message or Folder path.
        """
        paths_found: List[Path] = self.folder_path
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
    def folders_in_home_dir(self, directory: str) -> Optional:
        """
        Function for running bash commands in certain directories to find directory paths that matches a given name.

        :param directory: Sets the directory to search inside for file.
        :return: Folder paths matched or Error message.
        """
        try:
            search: subprocess.Popen[str] = subprocess.Popen(shlex.split(
                f"find ./{directory} -iname '{self.folder_name}' -type d "),
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
    """
    Contains functions for finding file paths.
    """
    def __init__(self, file_name: str, file_extensions: List[str]) -> None:
        """
        Initializes Class.

        :param file_name: Sets name of file.
        :param file_extensions: Sets the file extensions supported.
        """
        self.list_commands: List[str] = []
        self.file_name: str = file_name
        self.file_extensions: List[str] = file_extensions
        self.file_path: List[Path] = []

    @lru_cache
    def find_file_paths(self) -> Optional:
        """
        Function for finding file paths that matches the specified file name.

        :return: File path or Error message.
        """
        extensions: List[str] = self.file_extensions

        """
        - A for loop is executed based on the total number of elements in the :extension list:.
        - If the number of elements in the :extensions: list equals 1, then remove one element from 
            the :extensions: list and append the :data: to the :self.list_commands: list.
        - If the number of elements in the :extensions: list is more than 1, then remove two elements from 
            the :extensions: list (one using positive index of 0 and one using negative index -1) and append 
                the :data: to the :self.list_commands: list.
        - Break the loop if an error is encountered.
        """
        for i in range(len(extensions)):
            try:
                if len(extensions) == 1:
                    data: str = f"-iname '*{self.file_name}*{extensions[0]}' -type f"
                    extensions.pop(0)
                    self.list_commands.append(data)
                else:
                    data: str = f"\( -iname '*{self.file_name}*{extensions[0]}' -or -iname '*{self.file_name}*{extensions[-1]}' -type f \) -or"
                    extensions.pop(0), extensions.pop(-1)
                    self.list_commands.append(data)
            except IndexError:
                break

        directories: List[str] = ["Documents", "Music",
                                  "Videos", "Downloads", "Pictures"]

        file_path: List = []
        # Execute a for loop based on the total elements in the :directories: list,
        # then assign each element to the :self.files_in_home_dir: method.
        for i in directories:
            data: List[Path] = self.files_in_home_dir(i)
            if type(data) == list:
                file_path += data
            continue

        if len(file_path) == 0:
            return "File does not exist."

        self.file_path = file_path
        return self.choose_path()

    @lru_cache
    def choose_path(self) -> Optional:
        """
        Function for choosing the preferred path that matches a file name, if software finds more than one match.

        :return: Error message or File path.
        """
        paths_found: List[Path] = self.file_path
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
    def files_in_home_dir(self, directory: str) -> Optional:
        """
        Function for running bash commands in certain directories to find file paths that matches a given name.

        :param directory: Sets the directory to search inside for file.
        :return: File paths matched or Error message.
        """
        try:
            list_commands: List[str] = [f"find ./{directory}"] + self.list_commands
            command: str = " ".join(list_commands).rstrip("-or")

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
    configuration: Dict[str, str] = {}  # Variable for storing software's configurations.

    def __init__(self, configuration: Dict[str, str]) -> None:
        """
        Initializes Class.

        :param configuration: Dictionary object containing software's configurations.
        """
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
    """
    Contains functions for opening folder in either IDE or Folder Manager.
    """
    def __init__(self, search_keyword: str, folder_name: str) -> None:
        """
        Initializes Class.

        :param search_keyword: Sets command to either open folder in Folder Manager or edit folder in IDE.
        :param folder_name: Sets name of the folder.
        """
        super().__init__(Main.configuration)
        self.search_keyword: str = search_keyword
        self.folder_name: str = folder_name

    def run(self) -> Optional[str]:
        """
        Function for finding path of specified folder and assigning it to the open_with_ide_or_file_browser method.

        :return: Done or Error message
        """
        find_folder_path = FindFolderPath(self.folder_name).find_folder_paths()
        return self.open_with_ide_or_file_browser(find_folder_path) \
            if type(find_folder_path) is PosixPath or WindowsPath else find_folder_path

    def open_folder_in_ide(self, folder_path: Path) -> str:
        """
        Function for running bash command to open folder in IDE.

        :param folder_path: Sets absolute path for folder.
        :return: Done or Error message.
        """
        # Check if app is installed. Returns: Tuple containing a boolean value and a string
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
        """
        Function for running bash command to open folder in Folder Manager.

        :param folder_path: Sets absolute path for folder.
        :return: Done or Error message.
        """
        # Check if app is installed. Returns: Tuple containing a boolean value and a string
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
        """
        Function for selecting either to open folder in folder manager or to open in IDE
        based on the value for self.search_keyword variable.

        :param path: Sets absolute path for the searched folder if found.
        :return: Done or Error Message.
        """
        if 'browse folder' in self.search_keyword:
            return self.open_folder_in_file_browser(path)
        elif 'edit folder' in self.search_keyword:
            return self.open_folder_in_ide(path)
        return "Invalid command."


class OpenApp(Main):
    """
    Contains function for launching apps on the computer.
    """

    def __init__(self, search_keyword: str) -> None:
        """
        Initializes Class.

        :param search_keyword: Sets the name of the app to launch.
        """
        super().__init__(Main.configuration)
        self.search_keyword: str = search_keyword

    @lru_cache
    def launch_app(self) -> str:
        """
        Function for running bash command to launch application.
        Some apps can't open multiple windows of the app at the same time.

        :return: Done or Error message
        """
        app: str = self.search_keyword

        if (app_name := app.replace("-", "_").upper()) in Main.configuration:
            """
            - Check if app's name is in software's configuration dictionary object
            - If True, sets app to value in software's configuration dictionary object
            - Example: if app_name = "text editor", and app_name is found in Main.configuration, 
                then sets app_name to Gedit
            """
            app = Main.configuration[app_name]

        is_app_installed: Tuple[bool, str] = verify_app_installed(app)  # Returns: (bool, str)
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
    """
    Contains functions for watching videos or playing music.
    """
    def __init__(self, media_file_name: str) -> None:
        """
        Initializes Class.

        :param media_file_name: Sets the name of video or audio file.
        """
        super().__init__(Main.configuration)
        self.media_file_name: str = media_file_name

    @lru_cache
    def watch_video(self) -> str:
        """
        Function for running bash command to open video file with selected video player.

        :return: Done or Error message
        """
        supported_extensions = ['.mp4', '.mkv', '.avi']
        file_path: Path = FindFilePath(self.media_file_name, supported_extensions).find_file_paths()

        if type(file_path) is not (PosixPath or WindowsPath):
            return "Video file does not exist."

        if str(file_path).endswith(('.mp4', '.mkv', '.avi')) is False:
            return "Un-supported video file format."

        try:
            subprocess.Popen(shlex.split(f"{self.video_player} {file_path}"),
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.video_player} app not installed."

    @lru_cache
    def play_music(self) -> str:
        """
        Function for running bash command to open audio file with selected audio player.

        :return: Done or Error message
        """
        supported_extensions = ['.mp3', '.ogg']
        file_path: Path = FindFilePath(self.media_file_name, supported_extensions).find_file_paths()

        if type(file_path) is not (PosixPath or WindowsPath):
            return "Audio file does not exist."

        if str(file_path).endswith(('.mp3', '.ogg')) is False:
            return "Un-supported audio file format."

        try:
            subprocess.Popen(shlex.split(f"{self.music_player} {file_path}"),
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.music_player} app not installed."


@lru_cache
def totem_commands(command: str):
    """
    Function for running bash commands to control video playing in Totem app.

    :param command: Sets the application option.
    :return: Done or Error Message.
    """
    # A list of some of the application options supported by Totem app.
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
        """
        Bash Command applied -> totem option
        option: Sets the application option.
        """
        subprocess.Popen(shlex.split(f"totem {option}"),
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                         universal_newlines=True, cwd=basedir.home())
        return "Done"

    except FileNotFoundError:
        return "Videos app not installed."


class SearchOnline(Main):
    """
    Contains functions for searching words or location with Google in a browser.
    """
    def __init__(self, search_term: str) -> None:
        """
        Initializes Class.

        :param search_term: what to search for.
        """
        super().__init__(Main.configuration)
        self.keywords: str = search_term

    @lru_cache
    def search(self) -> None:
        """
        Function for searching words with Google in a browser.
        """
        url: str = f"https://www.google.com/search?q={self.keywords}"
        browse: webbrowser.BaseBrowser = webbrowser.get(self.web_browser)
        browse.open_new_tab(url)

    @lru_cache
    def locate(self) -> None:
        """
        Function for searching the location of a place with Google Maps in a browser.
        """
        url: str = f"https://www.google.com/maps/search/{self.keywords}"
        browse: webbrowser.BaseBrowser = webbrowser.get(self.web_browser)
        browse.open_new_tab(url)


class ViewFile(Main):
    """
    Contains functions for opening file in text editor or pdf reader.
    """
    def __init__(self, file_name: str) -> None:
        """
        Initializes Class.

        :param file_name: Sets the name of the file.
        """
        super().__init__(Main.configuration)
        self.file_name: str = file_name

    @lru_cache
    def selector(self) -> str:
        """
        Function for choosing either to open file in text editor or pdf reader.

        :return: Done or Error message.
        """
        supported_extensions = ['.txt', '.json', '.pdf', '.csv']
        file_path: Path = FindFilePath(self.file_name, supported_extensions).find_file_paths()

        if type(file_path) is not (PosixPath or WindowsPath):
            return "File does not exist."

        if str(file_path).endswith(('.txt', '.json', '.pdf', '.csv')) is True:
            if str(file_path).endswith('.pdf') is True:
                return self.open_file_in_pdf_reader(file_path)
            return self.open_file_in_text_editor(file_path)

        return "Un-supported file format."

    @lru_cache
    def open_file_in_text_editor(self, file_path: Path) -> str:
        """
        Function for running bash command to open a JSON, TXT or CSV file in a text editor.

        :param file_path: Absolute path of a JSON, TXT or CSV file.
        :return: Done or Error message.
        """
        # Check if app is installed. Returns: Tuple containing a boolean value and a string
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
        """
        Function for running bash command to open a PDF file in a pdf reader

        :param file_path: Absolute path of a PDF file.
        :return: Done or Error message.
        """
        # Check if app is installed. Returns: Tuple containing a boolean value and a string
        if verify_app_installed(self.pdf_reader)[0] is False:
            return f"{self.pdf_reader.capitalize()} not installed."
        try:
            subprocess.Popen(shlex.split(f"{self.pdf_reader} {file_path}"),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True, cwd=basedir.home())
            return "Done"

        except FileNotFoundError:
            return f"{self.pdf_reader.capitalize()} could not open."


class BasicCalculator(Main):
    def __init__(self, calculations: str):
        super().__init__(Main.configuration)
        self.calculations: str = calculations

    def figure_in_words_to_numbers(self):
        pass

    def get_operands_operators(self):
        # string_format1 = twenty-nine plus six (figures in words)
        # string_format2 = -10.89 plus 8.1 (figures in numbers)
        # operators = "times|plus|minus|divided by|modulo" ([a-z_]+? ??[a-z_\- ]*?)
        # pattern_for_num_in_words = rf"^([a-z]+? ??[a-z\- ]*?) ({operators}) ([a-z]+? ??[a-z\- ]*?)$"
        # pattern_for_num_in_numbers = rf"^([\d-]+?\.??[\d]*?) ({operators}) ([\d-]+?\.??[\d]*?)$"
        pass

    def perform_calculations(self):
        # bash_command = gnome-calculator -m basic --solve=12mod3
        pass


@lru_cache
def open_dir_in_terminal(folder_name: str) -> str:
    """
    Function for running bash command to open a specified folder in the terminal.

    :param folder_name: Sets the name of the folder.
    :return: Done or Error Message.
    """
    folder_path: Path = FindFolderPath(folder_name).find_folder_paths()
    # Check if app is installed. Returns: Tuple containing a boolean value and a string
    if verify_app_installed("gnome-terminal")[0] is False:
        return f"Gnome Terminal app not installed."
    try:
        """
        Bash Command applied -> gnome-terminal --working-directory=NAME_OF_DIRECTORY
        --working-directory: Sets the working directory.
        NAME_OF_DIRECTORY: Absolute path of directory.
        """
        subprocess.Popen(shlex.split(f"gnome-terminal --working-directory={folder_path}"),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, cwd=basedir.home())
        return "Done"

    except FileNotFoundError:
        return f"Gnome Terminal could not open."


@lru_cache
def disk_info() -> Tuple[str, str, str]:
    """
    Function that retrieves computer disk information.

    :returns: (Free disk space, Used disk space, Total disk space) in gigabytes.
    """
    disk_usage = shutil.disk_usage(basedir.home())
    gigabyte: int = 1_000_000_000
    free: float = (disk_usage.free / gigabyte) * 1
    used: float = (disk_usage.used / gigabyte) * 1
    total: float = (disk_usage.total / gigabyte) * 1
    return (f"Free space: {free.__round__(2)}Gb",
            f"Used space: {used.__round__(2)}Gb",
            f"Total space: {total.__round__(2)}Gb")
