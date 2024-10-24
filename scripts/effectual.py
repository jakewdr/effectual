import os
import json
import tomllib
import pathlib
import shutil
import zipfile
import python_minifier
from time import perf_counter
from distutils.dir_util import copy_tree


def pathLeaf(path) -> str:
    return str(os.path.split(path)[1]).strip()


def bundle(srcDirectory: str, outputDirectory: str, compressionLevel: int) -> None:
    """Creates a bundle from all python files in a directory

    Args:
        srcDirectory (str): The original python file directory
        outputDirectory (str): The output directory for the bundle
        compressionLevel (int): The level of compression from 0 to 9
    """

    shutil.rmtree(outputDirectory)  # Deletes current contents of output directory
    shutil.copytree(srcDirectory, outputDirectory)  # Copies source to output directory

    pythonFiles: list[str] = [
        str(entry).replace(
            os.sep, "/"
        )  # Appends a string of the file path with forward slashes
        for entry in pathlib.Path(
            outputDirectory
        ).iterdir()  # For all the file entries in the directory
        if ".py" in str(pathlib.Path(entry))
    ]  # If it is a verified file and is a python file
    if MINIFICATION == True:
        for file in pythonFiles:
            with open(file, "r+") as fileRW:
                minifiedCode = python_minifier.minify(
                    fileRW.read(), rename_locals=False, rename_globals=False, hoist_literals=False
                )  # I don't rename vars as that could cause problems when importing between files
                # Also no hoisting literals as that causes un-needed variable assignment
                fileRW.seek(0)
                fileRW.writelines(minifiedCode)
                fileRW.truncate()
                

    with open("./Pipfile", "rb") as file:
        packages: dict = (tomllib.load(file)).get("packages")

    try:
        with open("./.effectual_cache/dependencies.json", "x") as file:
            file.write("{\n\n}")
    except FileExistsError:
        pass
    with open("./.effectual_cache/dependencies.json", "r") as jsonFileRead:
        try:
            fileContents: dict = json.load(jsonFileRead)
        except:
            fileContents: dict = {}
        for key in packages:
            if fileContents == {} or key not in packages:
                if packages.get(key) == "*":
                    os.system(
                        f"pip install {key} --target ./.effectual_cache/cachedPackages"
                    )
                else:
                    os.system(
                        f"pip install {key}=={packages.get(key)} --target ./.effectual_cache/cachedPackages"
                    )
                fileContents.update({key: packages.get(key)})
                json.dump(
                    fileContents, open("./.effectual_cache/dependencies.json", "w")
                )

    with zipfile.ZipFile(
        f"{outputDirectory}bundle.py",
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=compressionLevel,
    ) as bundler:
        for file in pathlib.Path("./.effectual_cache/cachedPackages").rglob("*"):
            arcname = str(file).replace(os.sep, "/").replace(".effectual_cache/cachedPackages", "")
            if "__pycache__" not in str(file) and ".dist-info" not in str(file): # Don't want .pyc files as they can be platform specific
                bundler.write(file, arcname=arcname)
        for file in pythonFiles:
            bundler.write(file, arcname=pathLeaf(file))  # pathleaf is needed to not maintain folder structure
            os.remove(file)  # Clean up

if "__main__" in __name__:
    with open("./effectual.config.json", "r") as file:
        configData: dict = json.load(file)

        SOURCEDIRECTORY: str = configData.get("sourceDirectory")
        OUTPUTDIRECTORY: str = configData.get("outputDirectory")
        COMPRESSIONLEVEL: int = configData.get("compressionLevel")  # From 0-9
        MINIFICATION: bool = configData.get("minification")

    if not os.path.exists(OUTPUTDIRECTORY):
        os.makedirs(OUTPUTDIRECTORY)
        
    pathlib.Path("./.effectual_cache/cachedPackages").mkdir(parents=True, exist_ok=True)

    start = perf_counter()
    bundle(SOURCEDIRECTORY, OUTPUTDIRECTORY, COMPRESSIONLEVEL)
    end = perf_counter()

    print(f"Bundled in {end - start} seconds")
