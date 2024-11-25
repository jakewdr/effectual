import hashlib
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


def getAllHashes(sourceDirectory: Path) -> dict[str]:
    """Gets all hashes in directory

    Args:
        sourceDirectory (Path): Path to the python scripts

    Returns:
        dict[str]: Dictionary containing paths and hashes
    """
    hashDictionary: dict[str] = dict()
    for pyFile in sourceDirectory.glob("*.py"):
        hashDictionary[pyFile]: dict[str] = getFilehash(pyFile)

    return hashDictionary
