from coding_yusha.controller.core.unit import Unit


class Field:
    allies: list[Unit]
    enemies: list[Unit]

    def __init__(self, allies: list[Unit], enemies: list[Unit]):
        unit_names = [unit.name for unit in allies + enemies]
        if len(unit_names) != len(set(unit_names)):
            raise Exception("ユニットの名前が重複しています。")

        self.allies = allies
        self.enemies = enemies

    # def is_buttle_end(self) -> bool:
    #     are_allies_dead = all([ally.is_dead() for ally in self.allies])
    #     are_enemies_dead = all([enemy.is_dead() for enemy in self.enemies])
    #     return are_allies_dead or are_enemies_dead

    def _equals(self, other: "Field") -> bool:
        return (
            len(self.allies) == len(other.allies) and
            len(self.enemies) == len(other.enemies) and
            all(a._equals(b) for a, b in zip(self.allies, other.allies)) and
            all(e._equals(f) for e, f in zip(self.enemies, other.enemies))
        )
