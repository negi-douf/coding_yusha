from coding_yusha.controller.core.unit_record import UnitRecord

class Commentator():
    allies: list[UnitRecord]
    enemies: list[str]

    def update_allies(self, allies):
        self.allies = allies

    def update_enemies(self, enemies):
        self.enemies = enemies

    def get_enemies(self) -> list[str]:
        return self.enemies
