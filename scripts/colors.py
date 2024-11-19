from termcolor import colored
from pathlib import Path
import os


def fileColor(filePath: Path) -> str:
    return colored(f"{str(round(os.path.getsize(filePath) / 1024, 3))}kB", "yellow")


def tagColor(nameOfTag: str) -> str:
    return colored(f"[{nameOfTag.upper()}]", "blue")


def errorColor(errorString: str) -> str:
    return colored(errorString, "red")


def folderColor(sizeOfFolder: int) -> str:
    return colored(f"{round((sizeOfFolder / 1024), 3)}kB", "yellow")


def completeColor(completeString: str) -> str:
    return colored(completeString, "light_magenta")
