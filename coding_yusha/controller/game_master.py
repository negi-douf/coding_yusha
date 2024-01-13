from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.initialize_field import initialize_field


class GameMaster():
    field: Field

    def __init__(self, stage: str, *ally_py_files: str):
        print(ally_py_files)
        ally_py_list = list(ally_py_files)
        self.field = initialize_field(stage, ally_py_list)
