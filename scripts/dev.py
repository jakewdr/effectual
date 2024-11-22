import os
import zipfile
from pathlib import Path
from config import loadConfig
from datetime import datetime


def main() -> None:
    """Super fast bundling for the 'task dev' command"""

    configData = loadConfig(Path("./effectual.config.json"))
    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))

    Path("./.effectual_cache/dev/").mkdir(parents=True, exist_ok=True)
    currentTime: str = str(datetime.now().strftime(r"%d%m%Y%H%M%S"))
    outputFile: str = f"./.effectual_cache/dev/bundle.{currentTime}.py"

    with zipfile.ZipFile(outputFile, "w") as bundler:
        for pyFile in sourceDirectory.glob("*.py"):
            bundler.write(pyFile, arcname=pyFile.name)

    os.system(f"pipenv run python {outputFile}")


if __name__ == "__main__":
    main()
