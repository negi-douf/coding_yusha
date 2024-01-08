from coding_yusha.controller.core.field import Field

# from coding_yusha.controller.core.initialize_field import initialize_field

# from coding_yusha.controller.core.unit import Unit


class GameMaster():
    field: Field

    def __init__(self, stage: str, *ally_py_files: str):
        print(ally_py_files)
        # self.field = initialize_field(stage, ally_py_files)
