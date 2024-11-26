import hashlib
from multiprocessing import Pool
from pathlib import Path


def getFilehash(filePath: Path) -> str:
    """Gets the file hash of a single python script

    Args:
        filePath (Path): Path to the python script

    Returns:
        str: Hash of the python script
    """
    with open(filePath, "rb") as file:
        fileHash = hashlib.sha256(file.read()).hexdigest()
    return fileHash


def getAllHashes(sourceDirectory: Path) -> list[str]:
    """Gets all hashes in directory

    Args:
        sourceDirectory (Path): Path to the python scripts

    Returns:
        dict[str]: Dictionary containing paths and hashes
    """

    with Pool() as pool:
        hashList: list[str] = pool.map(getFilehash, sourceDirectory.glob("*.py"))
    return hashList
