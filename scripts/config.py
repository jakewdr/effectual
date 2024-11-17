from pathlib import Path
import simplejson


def loadConfig(configPath: Path) -> dict:
    """Loads a json file and dumps it to a dictionary

    Args:
        configPath (Path): Path to the configuration .json file

    Raises:
        RuntimeError: If the json is in an invalid format
        RuntimeError: If the json path can't be found

    Returns:
        dict: Dictionary with the contents of the .json file
    """
    try:
        with configPath.open("r") as configFile:
            return simplejson.load(configFile)
    except ValueError as e:
        raise RuntimeError(f"Invalid JSON in {configPath}: {e}")
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file {configPath} not found.")
