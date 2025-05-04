from coding_yusha.controller.core.unit_record import UnitRecord

class Commentator():
    allies: list[UnitRecord]
    enemies: list[str] # 敵の情報は名前のみ

    def update_allies(self, allies):
        self.allies = allies

    def update_enemies(self, enemies):
        self.enemies = enemies

    def get_allies(self) -> list[UnitRecord]:
        return self.allies

    def get_enemies(self) -> list[str]:
        return self.enemies

    def get_alive_allies(self) -> list[UnitRecord]:
        return [ally for ally in self.allies if ally.current_hp > 0]
