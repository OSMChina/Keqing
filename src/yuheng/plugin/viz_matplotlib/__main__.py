import os
import sys

import matplotlib

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "..", "..")
sys.path.append(src_dir)
from yuheng import Waifu
from yuheng.type import Node, Relation, Way


def init(N, W, S, E):
    pass


def main() -> None:
    print("This plugin can't be run as module.")


if __name__ == "__main__":
    main()
