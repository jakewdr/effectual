import rtoml


def loadConfig(configPath: str) -> dict:
    try:
        with open(configPath, "r", encoding="utf-8") as file:
            tomlFile: dict = dict(rtoml.load(file))
            configData: dict = tomlFile.get("tool").get("effectual")
    except ValueError as e:
        raise RuntimeError(f"Invalid TOML in {configPath}: {e}")
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file {configPath} not found.")

    return configData
