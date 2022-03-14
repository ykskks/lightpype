from datetime import datetime
from pathlib import Path

from lightpype import Pipeline, Script

LOGDIR_NAME = ".lightpype"
LOGFILE_NAME = "log.json"


def _make_sample_script(srcdir, filename: str):  # -> py.path.local
    script = srcdir.join(f"{filename}.py")
    script.write(f"print('{filename}')")
    return script


class TestPipeline:
    def test_first_run(self, tmpdir, capfd):
        srcdir = tmpdir.mkdir("src")

        first_py = _make_sample_script(srcdir, "first")
        second_py = _make_sample_script(srcdir, "second")

        scripts = [
            Script(Path(first_py)),
            Script(Path(second_py)),
        ]

        pipeline = Pipeline(scripts, Path(tmpdir))
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == "first\nsecond\n"

    def test_no_execution(self, tmpdir, capfd):
        srcdir = tmpdir.mkdir("src")

        first_py = _make_sample_script(srcdir, "first")
        second_py = _make_sample_script(srcdir, "second")

        logfile = tmpdir.mkdir(LOGDIR_NAME).join(LOGFILE_NAME)
        logfile.write('{"last_executed_at": ' + f'"{str(datetime.now())}"' + "}")

        scripts = [
            Script(Path(first_py)),
            Script(Path(second_py)),
        ]

        pipeline = Pipeline(scripts, Path(tmpdir))
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == ""

    def test_only_second(self, tmpdir, capfd):
        srcdir = tmpdir.mkdir("src")

        first_py = _make_sample_script(srcdir, "first")

        logfile = tmpdir.mkdir(LOGDIR_NAME).join(LOGFILE_NAME)
        logfile.write('{"last_executed_at": ' + f'"{str(datetime.now())}"' + "}")

        second_py = _make_sample_script(srcdir, "second")

        scripts = [
            Script(Path(first_py)),
            Script(Path(second_py)),
        ]

        pipeline = Pipeline(scripts, Path(tmpdir))
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == "second\n"
