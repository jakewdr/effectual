from build import minifyFile
import tomllib
import pathlib
import json
import os


def main() -> None:
    """Entrypoint to the automatic package installer

    Raises:
        Exception: In the even the config file can't be found
    """
    with open("./Pipfile", "rb") as file:
        packages: dict = dict((tomllib.load(file)).get("packages"))

    with open("./effectual.config.json", "r") as file:
        try:
            configData: dict = json.load(file)
        except ValueError:
            raise Exception("Failed to load effectual.config.json")

    MINIFY: bool = configData.get("minification")

    arguments: list[str] = ["--no-compile", "--quiet", "--upgrade", "--no-binary=none"]

    argumentString: str = " ".join(arguments)

    for key in packages:
        print(f"Installing {key}")
        pathToInstallTo: str = "./.effectual_cache/cachedPackages"
        if packages.get(key) == "*":
            os.system(
                f"pipenv run pip install {key} {argumentString} --target {pathToInstallTo}"
            )
        else:
            os.system(
                f"pipenv run pip install {key}=={packages.get(key)} {argumentString} --target {pathToInstallTo}"
            )

    print("Finished installing current dependencies")

    for file in pathlib.Path("./.effectual_cache/cachedPackages").rglob("*"):
        if (
            "__pycache__" in str(file)
            or ".dist-info" in str(file)
            or ".pyc" in str(file)
            or ".pyd" in str(file)
            or "normalizer.exe" in str(file)
            or "py.typed" in str(file)
        ):
            try:
                os.remove(str(file))
            except PermissionError:
                pass

        if str(file).endswith(".py") and MINIFY:
            minifyFile(file)
    print("Finished optimizing dependencies")


if __name__ == "__main__":
    main()
