from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import argv
from typing import Final

_DEFAULT_PATH: Final[str] = "./migrations/versions"


def main() -> str:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", type=Path, default=_DEFAULT_PATH)
    namespace: Namespace = parser.parse_args(argv[1:])
    return "{:03}".format(len(list(namespace.path.glob("*.py"))) + 1)


if __name__ == "__main__":
    print(main())  # noqa: T201
