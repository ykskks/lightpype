import time
from datetime import datetime
from pathlib import Path

from lightpype import Pipeline, Script

SRCDIR_NAME = "src"
LOGDIR_NAME = ".lightpype"
LOGFILE_NAME = "log.json"


def _make_sample_script(tmpdir: Path, filename: str) -> Path:
    srcdir = tmpdir / "src"
    srcdir.mkdir(exist_ok=True)

    script = srcdir / f"{filename}.py"
    script.write_text(f"print('{filename}')")
    return script


def _make_sample_logfile(tmpdir: Path):
    logfile = tmpdir / LOGDIR_NAME / LOGFILE_NAME
    logfile.parent.mkdir(parents=True, exist_ok=True)

    logfile.write_text('{"last_executed_at": ' + f'"{str(datetime.now())}"' + "}")


class TestPipeline:
    def test_first_run(self, tmpdir, capfd):
        tmpdir = Path(tmpdir)

        first_py = _make_sample_script(tmpdir, "first")
        second_py = _make_sample_script(tmpdir, "second")

        scripts = [
            Script(first_py),
            Script(second_py),
        ]

        pipeline = Pipeline(scripts, tmpdir)
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == "first\nsecond\n"

    def test_no_execution(self, tmpdir, capfd):
        tmpdir = Path(tmpdir)

        first_py = _make_sample_script(tmpdir, "first")
        second_py = _make_sample_script(tmpdir, "second")

        _make_sample_logfile(tmpdir)

        scripts = [
            Script(first_py),
            Script(second_py),
        ]

        pipeline = Pipeline(scripts, tmpdir)
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == ""

    def test_only_second(self, tmpdir, capfd):
        tmpdir = Path(tmpdir)

        first_py = _make_sample_script(tmpdir, "first")

        _make_sample_logfile(tmpdir)
        time.sleep(1.0)  # make sure the logfile is written first

        second_py = _make_sample_script(tmpdir, "second")

        scripts = [
            Script(first_py),
            Script(second_py),
        ]

        pipeline = Pipeline(scripts, tmpdir)
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == "second\n"
