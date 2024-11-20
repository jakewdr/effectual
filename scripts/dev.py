import subprocess
import zipfile
from pathlib import Path
from config import loadConfig
from random import getrandbits


def main() -> None:
    """Super fast bundling for the 'task dev' command"""

    configData = loadConfig(Path("./effectual.config.json"))

    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))

    Path("./.effectual_cache/dev/").mkdir(parents=True, exist_ok=True)
    outputFile: str = f"./.effectual_cache/dev/bundle.{str(getrandbits(16))}.py"

    with zipfile.ZipFile(outputFile, "w") as bundler:
        for pyFile in sourceDirectory.glob("*.py"):
            bundler.write(pyFile, arcname=pyFile.name.strip())

    subprocess.run(["pipenv", "run", "python", outputFile], check=True)


if __name__ == "__main__":
    main()
