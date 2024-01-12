from argparse import ArgumentParser

from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.initialize_field import initialize_field

# from coding_yusha.controller.core.unit import Unit


class GameMaster():
    field: Field

    def __init__(self, stage: str, *ally_py_files: str):
        print(ally_py_files)
        ally_py_list = list(ally_py_files)
        self.field = initialize_field(stage, ally_py_list)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("stage", help="ステージ名")
    parser.add_argument("ally_py_files", nargs="+", help="味方のユニットのファイルパス")
    args = parser.parse_args()
    GameMaster(args.stage, *args.ally_py_files)
