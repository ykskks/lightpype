# lightpype

lightpype is a lightweight Python library for pipeline management.

## Installation

```bash
pip install lightpype
```

## Usage

Usage example is provided in example direcotry.

```python
from pathlib import Path

from lightpype import Pipeline, Script

ROOT_DIR = Path(__file__).parents[1]
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
```

## WIP

- List executed scripts before the actual execution.
- Add options to enable customization.

## For developers

```bash
# setup
pip install -r requirements-dev.txt
pre-commit install

# run tests
pytest
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
