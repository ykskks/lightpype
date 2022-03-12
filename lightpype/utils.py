import json
from pathlib import Path


def load_json(filepath: Path) -> dict:
    """load json file and return dict.

    Args:
        filepath (Path): filepath to json file.

    Returns:
        dict: dict loaded from json file.
    """
    with open(filepath, "r") as f:
        obj = json.load(f)
    return obj


def dump_json(obj: dict, filepath: Path) -> None:
    """dump dict to json file.

    Args:
        obj (dict): dict to dump.
        filepath (Path): filepath to json file.

    Returns:
        None
    """
    with open(filepath, "w") as f:
        json.dump(obj, f, indent=4)
