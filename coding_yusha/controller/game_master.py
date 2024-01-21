from random import shuffle

from coding_yusha.controller.core import generate_unit, parse_assets
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


class GameMaster():
    field: Field
    stage_info: dict
    ally_file_map: dict
    enemy_file_map: dict
    turn_num: int = 0
    is_buttle_end: bool = False

    def __init__(self, stage: str, *ally_py_files: str):
        self.stage_info = parse_assets.load_stage_info(stage)
        ally_py_list = list(ally_py_files)
        self.ally_file_map = parse_assets.map_ally_files(self.stage_info, ally_py_list)
        self.enemy_file_map = parse_assets.map_enemy_files(self.stage_info)
        allies = generate_unit.generate_allies(self.ally_file_map)
        enemies = generate_unit.generate_enemies(self.enemy_file_map)
        self.field = Field(allies, enemies)
        self.print_stage_info()

    def decide_action_order(self) -> [Unit]:
        units = self.field.allies + self.field.enemies
        # 同じ素早さのユニットはランダムに並べたいため、都度シャッフルする
        shuffle(units)
        units_ordered = sorted(units, key=lambda unit: unit.agi, reverse=True)
        return units_ordered

    def print_stage_info(self):
        print("【戦闘開始】")
        print(f"ステージ: {self.stage_info['stage']}")
        print(f"敵: {[enemy.name for enemy in self.field.enemies]}")
        print(f"味方: {[ally.name for ally in self.field.allies]}")

    def wait_for_next_turn(self):
        valid_commands = ["i", "w"]
        # buttle, info, withdraw, help
        command = input("> ")
        while command not in valid_commands:
            print(f"有効なコマンドは {valid_commands} です")
            command = input("> ")
        if command == "i":
            self.print_info()
        if command == "w":
            self.is_buttle_end = True

    def print_info(self):
        print(f"ステージ: {self.stage_info['stage']}")
        print(f"ターン: {self.turn_num}")
        for enemy in self.field.enemies:
            if enemy.is_dead():
                print(f"{enemy.name}: HP 0/{enemy.max_hp}, MP ?/?")
            else:
                print(f"{enemy.name}: HP ?/?, MP ?/?")
        for ally in self.field.allies:
            print(f"{ally.name}: HP {ally.current_hp}/{ally.max_hp}, "
                  "MP {ally.current_mp}/{ally.max_mp}")
