from __future__ import annotations  # for Python3.7

import json
import subprocess
from datetime import datetime
from pathlib import Path

LOGDIR_NAME = ".lightpype"
LOGFILE_NAME = "log.json"


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


class Script:
    def __init__(self, filepath: Path):
        self.filepath = filepath

    @property
    def last_modified_at(self) -> datetime:
        """returns last modified datetime.

        Returns:
            datetime: last modified datetime.
        """
        return datetime.fromtimestamp(self.filepath.stat().st_mtime)

    def run(self) -> None:
        """run script.

        Returns:
            None
        """
        subprocess.call(["python", self.filepath], shell=False)


class Pipeline:
    def __init__(self, scripts: list[Script], rootdir: Path):
        self.scripts = scripts
        self.rootdir = rootdir

    def run(self) -> None:
        """run pipeline."""
        logdir = self.rootdir / LOGDIR_NAME
        logdir.mkdir(exist_ok=True)

        try:
            excution_log = load_json(logdir / LOGFILE_NAME)
        except FileNotFoundError:
            excution_log = None

        # when pipline is first run
        if excution_log is None:
            for script in self.scripts:
                script.run()

        else:
            last_exceuted_at = datetime.strptime(
                excution_log["last_excuted_at"], "%Y-%m-%d %H:%M:%S.%f"
            )
            for i, script in enumerate(self.scripts):
                if last_exceuted_at <= script.last_modified_at:

                    # run all scripts after last modified script
                    for script in self.scripts[i:]:
                        script.run()

                    break

        dump_json({"last_excuted_at": str(datetime.now())}, logdir / LOGFILE_NAME)
