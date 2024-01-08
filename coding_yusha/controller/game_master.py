from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


class GameMaster():
    field: Field

    def __init__(self, stage: str, *ally_py_files: str):
        print(ally_py_files)
        ally_01 = Unit("test", "ally_01.yml")
        ally_02 = Unit("test", "ally_02.yml")
        allies = [ally_01, ally_02]
        enemies = [Unit("test", "enemy_01.yml")]
        self.field = Field(allies, enemies)
