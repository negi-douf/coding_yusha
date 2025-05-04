from coding_yusha.controller.core.unit_record import UnitRecord

class Commentator():
    all_allies: list[UnitRecord]
    alive_allies: list[UnitRecord]
    all_enemies: list[str] # 敵の情報は名前のみ
    allive_enemies: list[str]

    def update_all_allies(self, allies):
        self.all_allies = allies

    def update_all_enemies(self, enemies):
        self.all_enemies = enemies

    def get_all_allies(self) -> list[UnitRecord]:
        return self.all_allies

    def get_all_enemies(self) -> list[str]:
        return self.all_enemies

    def get_alive_allies(self) -> list[UnitRecord]:
        return [ally for ally in self.all_allies if ally.current_hp > 0]
