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

    def _get_execute_from_index(self, last_executed_at: datetime) -> int:
        """get index of script to execute from.

        Args:
            last_executed_at (datetime): datetime of last execution.

        Returns:
            int: index of script to execute from.
        """

        for i, script in enumerate(self.scripts):
            if last_executed_at <= script.last_modified_at:
                return i

        # when no file was modified after last execution
        return -1

    def run(self) -> None:
        """run pipeline."""
        logdir = self.rootdir / LOGDIR_NAME
        logdir.mkdir(exist_ok=True)

        try:
            execution_log = load_json(logdir / LOGFILE_NAME)
        except FileNotFoundError:
            execution_log = None

        # when pipline is first run
        if execution_log is None:
            for script in self.scripts:
                script.run()

        else:
            last_executed_at = datetime.strptime(
                execution_log["last_executed_at"], "%Y-%m-%d %H:%M:%S.%f"
            )

            execute_from = self._get_execute_from_index(last_executed_at)

            for script in self.scripts[execute_from:]:
                script.run()

        dump_json({"last_executed_at": str(datetime.now())}, logdir / LOGFILE_NAME)
