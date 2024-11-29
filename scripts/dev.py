import subprocess
import time
import zipfile
from pathlib import Path

from colors import completeColor, fileColor, tagColor
from config import loadConfig
from fileHash import getAllHashes


def bundle(sourceDirectory: Path, outputFile: Path) -> None:
    """Bundles scripts into a single .py archive

    Args:
        sourceDirectory (Path): Path to the original python scripts
    """
    startTime = time.perf_counter()

    with zipfile.ZipFile(outputFile, "w") as bundler:
        for pyFile in sourceDirectory.rglob("*.py"):
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            bundler.write(pyFile, arcname=pyFile.name)
    endTime = time.perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


def main() -> None:
    """Super fast bundling for the 'task dev' command"""

    configData: dict = loadConfig("./pyproject.toml")
    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))
    outputFileName: str = Path(configData.get("outputFileName", "bundle.pyz"))
    devBundlePath: Path = Path("./.effectual_cache/dev/")
    devBundlePath.mkdir(parents=True, exist_ok=True)

    outputFile: Path = devBundlePath / outputFileName

    bundle(sourceDirectory, outputFile)

    runCommand = subprocess.Popen(["uv", "run", outputFile], shell=True)

    lastHashList: list[str] = getAllHashes(sourceDirectory)

    while True:
        currentHashList: list[str] = getAllHashes(sourceDirectory)
        if currentHashList != lastHashList:
            lastHashList = currentHashList
            runCommand.kill()
            runCommand.wait()
            outputFile.unlink()
            print(f"{tagColor('reloaded')}   || file change detected")
            bundle(sourceDirectory)
            runCommand = subprocess.Popen(["uv", "run", outputFile], shell=True)
        else:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
