from random import shuffle

from coding_yusha.controller.core import generate_unit, parse_assets
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


class GameMaster():
    field: Field
    stage_info: dict
    ally_file_map: dict
    enemy_file_map: dict

    def __init__(self, stage: str, *ally_py_files: str):
        self.stage_info = parse_assets.load_stage_info(stage)
        ally_py_list = list(ally_py_files)
        self.ally_file_map = parse_assets.map_ally_files(self.stage_info, ally_py_list)
        self.enemy_file_map = parse_assets.map_enemy_files(self.stage_info)
        allies = generate_unit.generate_allies(self.ally_file_map)
        enemies = generate_unit.generate_enemies(self.enemy_file_map)
        self.field = Field(allies, enemies)

    def is_buttle_end(self) -> bool:
        are_allies_dead = all([ally.is_dead() for ally in self.field.allies])
        are_enemies_dead = all([enemy.is_dead() for enemy in self.field.enemies])
        return are_allies_dead or are_enemies_dead

    def decide_action_order(self) -> [Unit]:
        units = self.field.allies + self.field.enemies
        # 同じ素早さのユニットはランダムに並べたいため、都度シャッフルする
        shuffle(units)
        units_ordered = sorted(units, key=lambda unit: unit.agi, reverse=True)
        return units_ordered
