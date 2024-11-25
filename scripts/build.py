import os
import shutil
import zipfile
from multiprocessing import Pool
from pathlib import Path
from time import perf_counter

import rtoml
from colors import completeColor, fileColor, folderColor, tagColor
from config import loadConfig
from fileHash import getFilehash
from minification import minifyFile, minifyToString


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

        print(
            f"{tagColor('bundling')}   || Pipenv dependencies {folderColor(totalSize)}"
        )

        for pyFile in sourceDirectory.glob("*.py"):
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            if minification:
                fileContents = minifyToString(pyFile)
                bundler.writestr(zinfo_or_arcname=pyFile.name, data=fileContents)
            else:
                bundler.write(pyFile, arcname=pyFile.name)

    print(f"{tagColor('OUTPUT')}     || {outputFileName} {fileColor(outputPath)}")


def dependencies(minify: bool) -> None:
    with open("./Pipfile", "r", encoding="utf-8") as file:
        packages: dict = dict((rtoml.load(file)).get("packages"))

    arguments: list[str] = ["--no-compile", "--quiet", "--no-binary=none", "--no-cache"]

    pathToInstallTo: str = "./.effectual_cache/cachedPackages"
    argumentString: str = " ".join(arguments)

    if Path(pathToInstallTo).exists():
        shutil.rmtree(pathToInstallTo)

    for key in packages:
        print(f"{tagColor('installing')} || {key}")
        if packages.get(key) != "*":
            key = f"{key}=={packages.get(key)}"
        os.system(
            f"pipenv run pip3 install {key} {argumentString} --target {pathToInstallTo}"
        )

    with Pool() as pool:
        print(f"{tagColor('optimizing')} || {','.join(packages)}")
        pool.map(
            optimizeDependencies,
            Path("./.effectual_cache/cachedPackages").rglob("*"),
            minify,
        )


def optimizeDependencies(file: Path) -> None:
    """Removes files not needed and if minifies if true

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

        if file.suffix == ".py" and minification:
            minifyFile(file)


def main() -> None:
    """Entrypoint

    Raises:
        RuntimeError: In the event there is no source directory
    """

    configData: dict = loadConfig("./pyproject.toml")

    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))
    outputDirectory: Path = Path(configData.get("outputDirectory", "out/"))
    outputFileName: str = configData.get("outputFileName", "bundle.py")
    compressionLevel: int = max(
        0, min(9, configData.get("compressionLevel", 5))
    )  # Default level if not set
    global minification
    minification = configData.get("minification", True)

    if not sourceDirectory.is_dir():
        raise RuntimeError(
            f"Source directory {sourceDirectory} does not exist or is not a directory."
        )

    pipfileHashPath: Path = Path("./.effectual_cache/pipfileHash.toml")
    currentHash: dict[str] = dict()

    startTime = perf_counter()

    Path("./.effectual_cache/").mkdir(parents=True, exist_ok=True)
    currentHash["hashes"]: dict[dict] = dict()
    currentHash["hashes"]["Pipfile"] = getFilehash("./Pipfile")
    currentHash["hashes"]["lock"] = getFilehash("./Pipfile.lock")

    if pipfileHashPath.exists():
        with open(pipfileHashPath, "r") as file:
            lastHash: dict = dict(rtoml.load(file)).get("hashes")

        if currentHash["hashes"] != lastHash:
            with open(pipfileHashPath, "w") as file:
                rtoml.dump(currentHash, file)
            dependencies(minify=minification)
    else:
        with open(pipfileHashPath, "x") as file:
            rtoml.dump(currentHash, file)
        dependencies(minify=minification)

    bundleFiles(
        sourceDirectory,
        outputDirectory,
        outputFileName,
        compressionLevel,
        minification,
    )
    endTime = perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


if "__main__" in __name__:
    main()
