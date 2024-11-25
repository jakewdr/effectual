import time
import rtoml
import hashlib
import zipfile
import subprocess
from pathlib import Path
from colors import tagColor, fileColor, completeColor
from datetime import datetime


def getFilehash(filePath: Path) -> str:
    """Gets the file hash of a single python script

    Args:
        filePath (Path): Path to the python script

    Returns:
        str: Hash of the python script
    """
    with open(filePath, "rb") as file:
        fileHash = hashlib.sha256(file.read()).hexdigest()
    return fileHash


def getAllHashes(sourceDirectory: Path) -> dict[str]:
    """Gets all hashes in directory

    Args:
        sourceDirectory (Path): Path to the python scripts

    Returns:
        dict[str]: Dictionary containing paths and hashes
    """
    hashDictionary: dict[str] = dict()
    for pyFile in sourceDirectory.glob("*.py"):
        hashDictionary[pyFile]: dict[str] = getFilehash(pyFile)

    return hashDictionary


def bundle(sourceDirectory: Path) -> None:
    """Bundles scripts into a single .py archive

    Args:
        sourceDirectory (Path): Path to the original python scripts
    """
    startTime = time.perf_counter()
    currentTime: str = str(datetime.now().strftime(r"%d%m%Y%H%M%S"))
    global outputFile
    outputFile = f"./.effectual_cache/dev/bundle.{currentTime}.py"

    with zipfile.ZipFile(outputFile, "w") as bundler:
        for pyFile in sourceDirectory.glob("*.py"):
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            bundler.write(pyFile, arcname=pyFile.name)
    endTime = time.perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


def main() -> None:
    """Super fast bundling for the 'task dev' command"""

    with open("./pyproject.toml", "r", encoding="utf-8") as file:
        configData: dict = dict((rtoml.load(file)).get("tool").get("effectual"))
    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))

    Path("./.effectual_cache/dev/").mkdir(parents=True, exist_ok=True)

    bundle(sourceDirectory)

    runCommand = subprocess.Popen(["pipenv", "run", "python", outputFile], shell=True)

    lastHashDict: dict[str] = getAllHashes(sourceDirectory)

    while True:
        currentHashDict = getAllHashes(sourceDirectory)
        if currentHashDict != lastHashDict:
            lastHashDict = currentHashDict
            runCommand.terminate()
            print(f"{tagColor('reloaded')}   || file change detected")
            bundle(sourceDirectory)
            runCommand = subprocess.Popen(
                ["pipenv", "run", "python", outputFile], shell=True
            )
        else:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
