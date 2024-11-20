from termcolor import colored
from pathlib import Path


def fileColor(filePath: Path) -> str:
    """Creates a yellow string with the size of a file

    Args:
        filePath (Path): Path to the file

    Returns:
        str: Output string
    """
    return colored(f"{str(round(filePath.stat().st_size / 1024, 3))}kB", "yellow")


def tagColor(nameOfTag: str) -> str:
    """Creates a blue tag with uppercase letters and squared brackets

    Args:
        nameOfTag (str): What the tag should be called

    Returns:
        str: Output string
    """
    return colored(f"[{nameOfTag.upper()}]", "blue")


def errorColor(errorString: str) -> str:
    """Makes an error string red

    Args:
        errorString (str):

    Returns:
        str: Output string
    """
    return colored(errorString, "red")


def folderColor(sizeOfFolder: int) -> str:
    """Writes out the size of a folder

    Args:
        sizeOfFolder (int): Size of the folder in bytes

    Returns:
        str: Output string
    """
    return colored(f"{round((sizeOfFolder / 1024), 3)}kB", "yellow")


def completeColor(completeString: str) -> str:
    """Makes a string light magenta

    Args:
        completeString (str): String to be shown at end of process

    Returns:
        str: Output string
    """
    return colored(completeString, "light_magenta")
