import os
import shutil
from pathlib import Path
import zipfile
from config import loadConfig
from minification import minifyFile
from colors import tagColor, fileColor, errorColor, folderColor, completeColor
from time import perf_counter


def bundleFiles(
    sourceDirectory: Path,
    outputDirectory: Path,
    outputFileName: str,
    compressionLevel: int,
    minification: bool,
) -> None:
    """Bundles dependencies and scripts into a single .py archive

    Args:
        sourceDirectory (Path): Source directory which must contain a __main__.py script
        outputDirectory (Path): Output directory for the bundle
        outputFileName (str): Name of the output bundle
        compressionLevel (int): Compression level for the bundle from 0-9
        minification (bool): If the dependencies and scripts should be minified
    """
    outputDirectory.mkdir(parents=True, exist_ok=True)
    outputPath: Path = outputDirectory / outputFileName

    if outputPath.exists():
        outputPath.unlink()

    startTime = perf_counter()

    pythonFiles: list[Path] = []
    for filePath in sourceDirectory.glob("*.py"):
        try:
            destination: Path = outputDirectory / filePath.name.strip()
            shutil.copyfile(filePath, destination)
            pythonFiles.append(destination)
        except PermissionError:
            print(errorColor(f"Skipped {filePath} due to permission error.", "red"))

    with zipfile.ZipFile(
        outputPath,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=compressionLevel,
    ) as bundler:
        cachePath: Path = Path("./.effectual_cache/cachedPackages")

        totalSize: int = int(0)
        for cachedFile in cachePath.rglob("*"):
            totalSize += os.path.getsize(cachedFile)
            arcName = cachedFile.relative_to(cachePath)
            bundler.write(cachedFile, arcname=arcName)

        print(f"{tagColor('bundling')} || Pipenv dependencies {folderColor(totalSize)}")

        for pyFile in pythonFiles:
            if minification:
                minifyFile(pyFile)

            print(f"{tagColor('bundling')} || {pyFile.name} {fileColor(pyFile)}")
            bundler.write(pyFile, arcname=pyFile.name.strip())
            pyFile.unlink()

    endTime = perf_counter()

    print(f"{tagColor('OUTPUT')}   || {outputPath.name} {fileColor(outputPath)}")
    print(completeColor(f"Bundled in {endTime - startTime:.3f}s"))


def main() -> None:
    """Entrypoint

    Raises:
        RuntimeError: In the event there is no source directory
    """
    configPath = Path("./effectual.config.json")
    configData = loadConfig(configPath)

    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))
    outputDirectory: Path = Path(configData.get("outputDirectory", "out/"))
    outputFileName: str = configData.get("outputFileName", "bundle.py")
    compressionLevel: int = configData.get(
        "compressionLevel", 9
    )  # Default level if not set
    minification: bool = configData.get("minification", True)

    if compressionLevel > 9:
        compressionLevel = 9
    elif compressionLevel < 0:
        compressionLevel = 0

    if not sourceDirectory.is_dir():
        raise RuntimeError(
            errorColor(
                f"Source directory {sourceDirectory} does not exist or is not a directory."
            )
        )

    bundleFiles(
        sourceDirectory=sourceDirectory,
        outputDirectory=outputDirectory,
        outputFileName=outputFileName,
        compressionLevel=compressionLevel,
        minification=minification,
    )


if "__main__" in __name__:
    main()
