import shutil
from pathlib import Path
import zipfile
from config import loadConfig
from minification import minifyFile
from time import perf_counter


def getFileName(path: Path) -> str:
    """Gets the filename from a path

    Args:
        path (Path): Pathlib path to file

    Returns:
        str: Filename
    """
    return path.name.strip()


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
    outputPath = outputDirectory / outputFileName

    if outputPath.exists():
        outputPath.unlink()

    startTime = perf_counter()

    pythonFiles: list[Path | str] = []
    for filePath in sourceDirectory.glob("*.py"):
        try:
            destination: Path | str = outputDirectory / getFileName(filePath)
            shutil.copyfile(filePath, destination)
            pythonFiles.append(destination)
        except PermissionError:
            print(f"Skipped {filePath} due to permission error.")

    with zipfile.ZipFile(
        outputPath,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=compressionLevel,
    ) as bundler:
        print("Bundling dependencies")
        for cachedFile in Path("./.effectual_cache/cachedPackages").rglob("*"):
            arcName = cachedFile.relative_to(".effectual_cache/cachedPackages")
            bundler.write(cachedFile, arcname=arcName)

        print("Bundling Python source files")
        for pyFile in pythonFiles:
            if minification:
                minifyFile(pyFile)
            bundler.write(pyFile, arcname=getFileName(pyFile))
            pyFile.unlink()

    endTime = perf_counter()
    print(f"Bundling completed in {endTime - startTime:.3f} seconds")


def main() -> None:
    """Entrypoint

    Raises:
        RuntimeError: In the even there is no source directory
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
            f"Source directory {sourceDirectory} does not exist or is not a directory."
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
