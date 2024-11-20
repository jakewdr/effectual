from pathlib import Path
import zipfile
from config import loadConfig
from minification import minifyToString
from colors import tagColor, fileColor, folderColor, completeColor
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

    with zipfile.ZipFile(
        outputPath,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=compressionLevel,
    ) as bundler:
        cachePath: Path = Path("./.effectual_cache/cachedPackages")

        totalSize: int = int(0)
        for cachedFile in cachePath.rglob("*"):
            if cachedFile.is_dir() and not any(cachedFile.iterdir()):
                continue
            totalSize += cachedFile.stat().st_size
            arcName = cachedFile.relative_to(cachePath)
            bundler.write(cachedFile, arcname=arcName)

        print(f"{tagColor('bundling')} || Pipenv dependencies {folderColor(totalSize)}")

        for pyFile in sourceDirectory.glob("*.py"):
            print(f"{tagColor('bundling')} || {pyFile.name} {fileColor(pyFile)}")
            if minification:
                fileContents = minifyToString(pyFile)
                bundler.writestr(
                    zinfo_or_arcname=pyFile.name, data=fileContents
                )
            else:
                bundler.write(pyFile, arcname=pyFile.name)

    endTime = perf_counter()

    print(f"{tagColor('OUTPUT')}   || {outputFileName} {fileColor(outputPath)}")
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
    compressionLevel: int = max(
        0, min(9, configData.get("compressionLevel", 5))
    )  # Default level if not set
    minification: bool = configData.get("minification", True)

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
