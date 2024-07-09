from random import shuffle

from coding_yusha.controller.core import generate_unit, parse_assets
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.proceed_event import proceed_event
from coding_yusha.controller.core.unit import Unit


class GameMaster():
    field: Field
    stage_info: dict
    ally_file_map: dict
    enemy_file_map: dict
    turn_num: int = 0
    won = False
    lost = False
    withdraw = False

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
        while not self.is_battle_end():
            self.wait_for_next_turn()
        self.print_result()

    def print_stage_info(self):
        print("【戦闘開始】")
        print(f"ステージ: {self.stage_info['stage']}")
        print(f"敵: {[enemy.name for enemy in self.field.enemies]}")
        print(f"味方: {[ally.name for ally in self.field.allies]}")
        print()

    def is_battle_end(self) -> bool:
        return self.withdraw or self.won or self.lost

    def update_battle_status(self):
        if all([ally.is_dead() for ally in self.field.allies]):
            self.lost = True
        elif all([enemy.is_dead() for enemy in self.field.enemies]):
            self.won = True

    def decide_action_order(self) -> list[Unit]:
        units = self.field.allies + self.field.enemies
        # 同じ素早さのユニットはランダムに並べたいため、都度シャッフルする
        shuffle(units)
        units_ordered = sorted(units, key=lambda unit: unit.agi, reverse=True)
        return units_ordered

    def wait_for_next_turn(self):
        self.reset_units()
        valid_commands = ["b", "i", "w"]
        # battle, info, withdraw, help
        command = input("> ")
        while command not in valid_commands:
            print(f"有効なコマンドは {valid_commands} です")
            command = input("> ")
        if command == "b":
            self.proceed_battle()
        elif command == "i":
            self.print_info()
        elif command == "w":
            self.withdraw = True

    def reset_units(self):
        for ally in self.field.allies:
            ally.reset_status()
        for enemy in self.field.enemies:
            enemy.reset_status()

    def proceed_battle(self):
        print(f"ターン: {self.turn_num}")
        units_ordered = self.decide_action_order()
        events = []
        for unit in units_ordered:
            if not unit.is_dead():
                event = unit.main()
                events.append(event)
        for event in events:
            proceed_event(event, self.field)
        print()
        self.update_battle_status()
        self.turn_num += 1

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
        if self.lost:
            print("敗北した...")
        elif self.won:
            print("勝利した！")
        else:
            print("撤退した")
        print(f"経過ターン数: {self.turn_num}")

    def get_allies_status(self):
        ally_replicas = []
        # NOTE: Unitに clone() みたいなメソッドを作ったほうがいいかも
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
        """Get enemies' replicas
        戦闘中の敵の状態を返す

        Args:
            all_ (bool, optional): 死んでいる敵も含めるかどうか. Defaults to False.
        """
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
