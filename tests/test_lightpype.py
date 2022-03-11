from datetime import datetime
from pathlib import Path

from lightpype import Pipeline, Script

LOGDIR_NAME = ".lightpype"
LOGFILE_NAME = "log.json"


class TestPipeline:
    def test_first_run(self, tmpdir, capfd):
        srcdir = tmpdir.mkdir("src")

        first_py = srcdir.join("first.py")
        first_py.write("print('first')")
        second_py = srcdir.join("second.py")
        second_py.write("print('second')")

        scripts = [
            Script(Path(first_py)),
            Script(Path(second_py)),
        ]

        pipeline = Pipeline(scripts, Path(tmpdir))
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == "first\nsecond\n"

    def test_no_exucution(self, tmpdir, capfd):
        srcdir = tmpdir.mkdir("src")

        first_py = srcdir.join("first.py")
        first_py.write("print('first')")
        second_py = srcdir.join("second.py")
        second_py.write("print('second')")

        logfile = tmpdir.mkdir(LOGDIR_NAME).join(LOGFILE_NAME)
        logfile.write('{"last_excuted_at": ' + f'"{str(datetime.now())}"' + "}")

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

        first_py = srcdir.join("first.py")
        first_py.write("print('first')")

        logfile = tmpdir.mkdir(LOGDIR_NAME).join(LOGFILE_NAME)
        logfile.write('{"last_excuted_at": ' + f'"{str(datetime.now())}"' + "}")

        second_py = srcdir.join("second.py")
        second_py.write("print('second')")

        scripts = [
            Script(Path(first_py)),
            Script(Path(second_py)),
        ]

        pipeline = Pipeline(scripts, Path(tmpdir))
        pipeline.run()

        # use capfd so that output from subprocesses are captured
        captured = capfd.readouterr()
        assert captured.out == "second\n"
