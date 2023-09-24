import argparse
import os
import sys


def main() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", type=str, default="./migrations/versions")
    namespace = parser.parse_args(sys.argv[1:])
    return "{:03}".format(len([p for p in os.listdir(namespace.path) if p.endswith(".py")]) + 1)


if __name__ == "__main__":
    print(main())  # noqa: T201
