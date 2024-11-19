from minification import minifyFile
from termcolor import colored
from pathlib import Path
from config import loadConfig
from multiprocessing import Pool
import shutil
import rtoml
import os


def optimizeDependencies(file: Path):
    """Removes files not needed and if minification is true minifies

    Args:
        file (Path): Path to a file in the effectual cache
    """
    stringFile: str = str(file)
    if (
        "__pycache__" in stringFile
        or ".dist-info" in stringFile
        or ".pyc" in stringFile
        or ".pyd" in stringFile
        or "normalizer.exe" in stringFile
        or "py.typed" in stringFile
    ):
        try:
            file.unlink()
        except PermissionError:
            pass

        if file.suffix == ".py" and MINIFY:
            minifyFile(file)


def main() -> None:
    """Entrypoint to the automatic package installer

    Raises:
        Exception: In the even the config file can't be found
    """
    with open("./Pipfile", "r", encoding="utf-8") as file:
        packages: dict = dict((rtoml.load(file)).get("packages"))

    arguments: list[str] = [
        "--no-compile",
        "--quiet",
        "--no-binary=none",
    ]

    pathToInstallTo: str = "./.effectual_cache/cachedPackages"
    argumentString: str = " ".join(arguments)

    shutil.rmtree(pathToInstallTo)

    for key in packages:
        print(f"{colored('[INSTALLING]', 'blue')} || {key}")
        if packages.get(key) == "*":
            os.system(
                f"pipenv run pip3 install {key} {argumentString} --target {pathToInstallTo}"
            )
        else:
            os.system(
                f"pipenv run pip3 install {key}=={packages.get(key)} {argumentString} --target {pathToInstallTo}"
            )

    with Pool() as pool:
        print(f"{colored('[OPTIMIZING]', 'blue')} || {','.join(packages)}")
        pool.map(
            optimizeDependencies, Path("./.effectual_cache/cachedPackages").rglob("*")
        )


if __name__ == "__main__":
    configPath: Path = Path("./effectual.config.json")
    configData: dict = loadConfig(configPath)

    MINIFY: bool = configData.get("minification")
    main()
