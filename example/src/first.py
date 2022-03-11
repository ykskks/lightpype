from pathlib import Path

ROOT_DIR = Path(__file__).parents[1]  # always returns absolute path in Python3.9+
DATA_PATH = ROOT_DIR / "data"
DATA_PATH.mkdir(exist_ok=True)


def main():
    with open(DATA_PATH / "first_out.txt", mode="w") as f:
        f.write("Hello world!")

    print("first exucuted.")


if __name__ == "__main__":
    main()
