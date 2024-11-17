import json
import shutil
from pathlib import Path
import zipfile
import python_minifier
from time import perf_counter


def getFileName(path: Path) -> str:
    """Gets the filename from a path

    Args:
        path (Path): Pathlib path to file

    Returns:
        str: Filename
    """
    return path.name.strip()


def minifyFile(filePath: Path) -> None:
    """Minifies a file from a certain path

    Args:
        filePath (Path): Path to the file to minify

    Raises:
        RuntimeError: In the event the file cannot be found or an error has ocurred
    """
    try:
        with filePath.open("r+") as fileRW:
            minifiedCode = python_minifier.minify(
                fileRW.read(),
                rename_locals=False,
                rename_globals=False,
                hoist_literals=False,
            )
            fileRW.seek(0)
            fileRW.writelines(minifiedCode)
            fileRW.truncate()
    except Exception as e:
        raise RuntimeError(f"Failed to minify {filePath}: {e}")


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

    pythonFiles = []
    for filePath in sourceDirectory.glob("*.py"):
        try:
            destination = outputDirectory / getFileName(filePath)
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
        print("Bundling dependencies...")
        for cachedFile in Path("./.effectual_cache/cachedPackages").rglob("*"):
            arcName = cachedFile.relative_to(".effectual_cache/cachedPackages")
            bundler.write(cachedFile, arcname=arcName)

        print("Bundling Python source files...")
        for pyFile in pythonFiles:
            if minification:
                minifyFile(pyFile)
            bundler.write(pyFile, arcname=getFileName(pyFile))
            pyFile.unlink()

    endTime = perf_counter()
    print(f"Bundling completed in {endTime - startTime:.3f} seconds")


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
            return json.load(configFile)
    except ValueError as e:
        raise RuntimeError(f"Invalid JSON in {configPath}: {e}")
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file {configPath} not found.")


def main() -> None:
    """Entrypoint

    Raises:
        RuntimeError: In the even there is no source directory
    """
    configPath = Path("./effectual.config.json")
    configData = loadConfig(configPath)

    sourceDirectory = Path(configData.get("sourceDirectory", "src/"))
    outputDirectory = Path(configData.get("outputDirectory", "out/"))
    outputFileName = configData.get("outputFileName", "bundle.py")
    compressionLevel = configData.get("compressionLevel", 9)  # Default level if not set
    minification = configData.get("minification", True)

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
