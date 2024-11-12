import tomllib
import os


def main() -> None:
    with open("./Pipfile", "rb") as file:
        packages: dict = dict((tomllib.load(file)).get("packages"))

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


if __name__ == "__main__":
    main()
