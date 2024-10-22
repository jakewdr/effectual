import os
import json
import tomllib
import pathlib
import shutil
import zipfile
import python_minifier
from time import perf_counter

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
        str(entry).replace(os.sep, "/")  # Appends a string of the file path with forward slashes
        for entry in pathlib.Path(outputDirectory).iterdir()  # For all the file entries in the directory
        if ".py" in str(pathlib.Path(entry))
    ]  # If it is a verified file and is a python file
    if MINIFICATION == True:
        for file in pythonFiles:
            with open(file, "r+") as fileRW:
                minifiedCode = python_minifier.minify(fileRW.read(), 
                    rename_locals=False, 
                    rename_globals=False
                ) # I don't rename vars as that could cause problems when importing between files
                fileRW.seek(0)
                fileRW.writelines(minifiedCode)
                fileRW.truncate()

    with open("./Pipfile", "rb") as file:
        packages: dict = tomllib.load(file)
        for key in packages.get("packages"):
            packageOutputPath = f"./dist/{key}"
            os.system(f"pip install {key} --target {packageOutputPath}")
            DEPENDENCIES.append(key)

    with zipfile.ZipFile(f"{outputDirectory}bundle.py", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=compressionLevel) as bundler:
        for file in pathlib.Path(outputDirectory).rglob("*"):
            arcname = str(file.relative_to(outputDirectory)).replace(os.sep, "/")
            for string in DEPENDENCIES:
                if f"{string}/" in arcname:
                    arcname = arcname.replace(f"{string}/", "", 1)
            if "bundle.py" not in str(file):
                bundler.write(
                    file,
                    arcname=arcname
                )
        
    ignore_set = {os.path.abspath(os.path.join(OUTPUTDIRECTORY, path)) for path in IGNORE}

    for root, dirs, files in os.walk(OUTPUTDIRECTORY, topdown=False):

        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))
            if file_path not in ignore_set:
                os.remove(file_path)

        for directory in dirs:
            directoryPath = os.path.abspath(os.path.join(root, directory))
            try:
                os.rmdir(directoryPath)
            except OSError:
                pass

if "__main__" in __name__:
    with open("./effectual.config.json", "r") as file:
        configData: dict = json.load(file)

        SOURCEDIRECTORY: str = configData.get("sourceDirectory")
        OUTPUTDIRECTORY: str = configData.get("outputDirectory")
        COMPRESSIONLEVEL: int = configData.get("compressionLevel") # From 0-9
        MINIFICATION: bool = configData.get("minification")
        IGNORE: list = ["bundle.py"]
        DEPENDENCIES: list = []

    if not os.path.exists(OUTPUTDIRECTORY):
        os.makedirs(OUTPUTDIRECTORY)
    start = perf_counter()
    bundle(SOURCEDIRECTORY, OUTPUTDIRECTORY, COMPRESSIONLEVEL)
    end = perf_counter()

    print(f"Bundled in {end - start} seconds")
