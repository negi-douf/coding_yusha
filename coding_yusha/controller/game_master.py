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

    def start(self):
        self.print_stage_info()
        while not self.is_buttle_end:
            self.wait_for_next_turn()
        self.print_result()

    def print_stage_info(self):
        print("【戦闘開始】")
        print(f"ステージ: {self.stage_info['stage']}")
        print(f"敵: {[enemy.name for enemy in self.field.enemies]}")
        print(f"味方: {[ally.name for ally in self.field.allies]}")
        print()

    def decide_action_order(self) -> [Unit]:
        units = self.field.allies + self.field.enemies
        # 同じ素早さのユニットはランダムに並べたいため、都度シャッフルする
        shuffle(units)
        units_ordered = sorted(units, key=lambda unit: unit.agi, reverse=True)
        return units_ordered

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
                  f"MP {ally.current_mp}/{ally.max_mp}")
        print()

    def print_result(self):
        if all([ally.is_dead() for ally in self.field.allies]):
            print("敗北した...")
        elif all([enemy.is_dead() for enemy in self.field.enemies]):
            print("勝利した！")
        else:
            print("撤退した")
        print(f"経過ターン数: {self.turn_num}")

    def get_allies_status(self):
        ally_replicas = []
        for ally in self.field.allies:
            replica = Unit()
            replica.name = ally.name
            replica.max_hp = ally.max_hp
            replica.current_hp = ally.current_hp
            replica.max_mp = ally.max_mp
            replica.current_mp = ally.current_mp
            replica.pa = ally.pa
            replica.pd = ally.pd
            replica.ma = ally.ma
            replica.md = ally.md
            replica.agi = ally.agi
            ally_replicas.append(replica)
        return ally_replicas

    def get_enemies(self, all_=False):
        enemy_replicas = []
        for enemy in self.field.enemies:
            if enemy.is_dead() and not all_:
                continue
            replica = Unit()
            # nameと is_dead() だけ使えるようにしたい
            replica.name = enemy.name
            if enemy.is_dead():
                replica.is_dead = lambda: True
            else:
                replica.is_dead = lambda: False
            enemy_replicas.append(replica)
        return enemy_replicas
