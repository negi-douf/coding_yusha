from coding_yusha.controller.core import initialize_field
from coding_yusha.controller.core.field import Field


class GameMaster():
    field: Field
    stage_info: dict

    def __init__(self, stage: str, *ally_py_files: str):
        self.stage_info = initialize_field.load_stage_info(stage)
        ally_py_list = list(ally_py_files)
        self.field = initialize_field.initialize_field(self.stage_info, ally_py_list)
