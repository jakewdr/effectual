import subprocess
import time
import zipfile
from pathlib import Path

from colors import completeColor, fileColor, tagColor
from config import loadConfig
from fileHash import getAllHashes


def bundle(sourceDirectory: Path) -> None:
    """Bundles scripts into a single .py archive

    Args:
        sourceDirectory (Path): Path to the original python scripts
    """
    startTime = time.perf_counter()

    outputFile: Path = Path("./.effectual_cache/dev/bundle.py")

    with zipfile.ZipFile(outputFile, "w") as bundler:
        for pyFile in sourceDirectory.rglob("*.py"):
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            bundler.write(pyFile, arcname=pyFile.name)
    endTime = time.perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


def main() -> None:
    """Super fast bundling for the 'task dev' command"""

    sourceDirectory: Path = Path(
        loadConfig("./pyproject.toml").get("sourceDirectory", "src/")
    )

    Path("./.effectual_cache/dev/").mkdir(parents=True, exist_ok=True)
    outputFile: Path = Path("./.effectual_cache/dev/bundle.py")

    bundle(sourceDirectory)

    runCommand = subprocess.Popen(["pipenv", "run", "python", outputFile], shell=True)

    lastHashDict: dict[str] = getAllHashes(sourceDirectory)

    while True:
        currentHashDict = getAllHashes(sourceDirectory)
        if currentHashDict != lastHashDict:
            lastHashDict = currentHashDict
            runCommand.kill()
            runCommand.wait()
            outputFile.unlink()
            print(f"{tagColor('reloaded')}   || file change detected")
            bundle(sourceDirectory)
            runCommand = subprocess.Popen(
                ["pipenv", "run", "python", outputFile], shell=True
            )
        else:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
