import os
import json
import shutil
import pathlib
import zipfile
import python_minifier
from time import perf_counter


def pathLeaf(path) -> str:
    return str(os.path.split(path)[1]).strip()


def minification(fileName: str) -> None:
    with open(fileName, "r+") as fileRW:
        minifiedCode = python_minifier.minify(
            fileRW.read(),
            rename_locals=False,
            rename_globals=False,
            hoist_literals=False,
        )  # I don't rename vars as that could cause problems when importing between files
        # Also no hoisting literals as that causes un-needed variable assignment
        fileRW.seek(0)
        fileRW.writelines(minifiedCode)
        fileRW.truncate()


def main() -> None:
    """Bundles python files and dependencies into a single file"""

    with open("./effectual.config.json", "r") as file:
        try:
            configData: dict = json.load(file)
        except ValueError:
            raise Exception("Failed to load effectual.config.json")

    SOURCEDIRECTORY: str = configData.get("sourceDirectory")
    OUTPUTDIRECTORY: str = configData.get("outputDirectory")
    OUTPUTFILENAME: str = configData.get("outputFileName")
    COMPRESSIONLEVEL: int = configData.get("compressionLevel")  # From 0-9
    MINIFICATION: bool = configData.get("minification")

    if not os.path.exists(OUTPUTDIRECTORY):
        os.makedirs(OUTPUTDIRECTORY)

    if os.path.exists(f"{OUTPUTDIRECTORY}/{OUTPUTFILENAME}"):
        os.remove(f"{OUTPUTDIRECTORY}/{OUTPUTFILENAME}")

    start = perf_counter()

    for entry in pathlib.Path(SOURCEDIRECTORY).iterdir():
        if ".py" in str(entry):
            try:
                shutil.copyfile(entry, f"{OUTPUTDIRECTORY}/{pathLeaf(entry)}")
            except PermissionError:
                pass
    pythonFiles: list[str] = [
        str(entry).replace(
            os.sep, "/"
        )  # Appends a string of the file path with forward slashes
        for entry in pathlib.Path(
            OUTPUTDIRECTORY
        ).iterdir()  # For all the file entries in the directory
        if ".py" in str(pathlib.Path(entry))
    ]  # If it is a verified file and is a python file

    with zipfile.ZipFile(
        f"{OUTPUTDIRECTORY}{OUTPUTFILENAME}",
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=COMPRESSIONLEVEL,
    ) as bundler:
        print("Bundling packages")
        for file in pathlib.Path("./.effectual_cache/cachedPackages").rglob("*"):
            arcname = (
                str(file)
                .replace(os.sep, "/")
                .replace(".effectual_cache/cachedPackages", "")
            )
            bundler.write(str(file), arcname=arcname)

        print("Bundling python source files")
        for file in pythonFiles:
            if MINIFICATION:
                minification(str(file))
            bundler.write(
                file, arcname=pathLeaf(file)
            )  # pathleaf is needed to not maintain folder structure
            os.remove(file)

    end = perf_counter()

    print(f"Bundled in {end - start:.3f} seconds")


if "__main__" in __name__:
    main()
