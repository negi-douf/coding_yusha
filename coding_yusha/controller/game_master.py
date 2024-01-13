from coding_yusha.controller.core import initialize_field
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


class GameMaster():
    field: Field
    stage_info: dict
    ally_files: dict
    enemy_files: dict

    def __init__(self, stage: str, *ally_py_files: str):
        self.stage_info = initialize_field.load_stage_info(stage)
        ally_py_list = list(ally_py_files)
        self.ally_files = initialize_field.map_ally_files(self.stage_info, ally_py_list)
        self.enemy_files = initialize_field.map_enemy_files(self.stage_info)
        allies = self.generate_allies()
        enemies = self.generate_enemies()
        self.field = Field(allies, enemies)

    def generate_allies(self):
        allies = []
        for ally in self.ally_files:
            _ally = Unit()
            _ally.attach_parameter(self.ally_files[ally]["yml"])
            allies.append(_ally)
        return allies

    def generate_enemies(self):
        enemies = []
        for enemy in self.enemy_files:
            _enemy = Unit()
            _enemy.attach_parameter(self.enemy_files[enemy]["yml"])
            enemies.append(_enemy)
        return enemies
