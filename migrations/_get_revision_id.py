from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import argv
from typing import Final

_DEFAULT_PATH: Final[str] = "./migrations/versions"


def get_next_revision_id(path: Path) -> int:
    return len(list(path.glob("*.py"))) + 1


def main() -> str:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", type=Path, default=_DEFAULT_PATH)
    namespace: Namespace = parser.parse_args(argv[1:])
    return "{id:03}".format(id=get_next_revision_id(path=namespace.path))


if __name__ == "__main__":
    print(main())  # noqa: T201
