from pathlib import Path
from python_minifier import minify


def minifyFile(filePath: Path, outputPath: Path) -> None:
    """Minifies a file from a certain path

    Args:
        filePath (Path): Path to the file to minify

    Raises:
        RuntimeError: In the event the file cannot be found or an error has occurred
    """
    try:
        with (
            filePath.open("r", encoding="utf-8") as fileR,
            outputPath.open("w", encoding="utf-8") as fileW,
        ):
            minifiedCode = minify(
                fileR.read(),
                rename_locals=False,
                rename_globals=False,
                hoist_literals=False,
            )
            fileW.write(minifiedCode)

    except Exception as e:
        raise RuntimeError(f"Failed to minify {filePath}: {e}")
