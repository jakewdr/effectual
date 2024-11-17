from pathlib import Path
from python_minifier import minify


def minifyFile(filePath: Path) -> None:
    """Minifies a file from a certain path

    Args:
        filePath (Path): Path to the file to minify

    Raises:
        RuntimeError: In the event the file cannot be found or an error has ocurred
    """
    try:
        with filePath.open("r+") as fileRW:
            minifiedCode = minify(
                fileRW.read(),
                rename_locals=False,
                rename_globals=False,
                hoist_literals=False,
            )
            fileRW.seek(0)
            fileRW.writelines(minifiedCode)
            fileRW.truncate()
    except Exception as e:
        raise RuntimeError(f"Failed to minify {filePath}: {e}")
