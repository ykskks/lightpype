from pathlib import Path

from lightpype import Pipeline, Script

ROOT_DIR = Path(__file__).parents[1]  # always returns absolute path in Python3.9+
SRC_PATH = ROOT_DIR / "src"
SRC_PATH.mkdir(exist_ok=True)


def main():
    scripts = [
        Script(SRC_PATH / "first.py"),
        Script(SRC_PATH / "second.py"),
    ]

    pipeline = Pipeline(scripts, ROOT_DIR)
    pipeline.run()


if __name__ == "__main__":
    main()
