from coding_yusha.controller.core.event_record import EventRecord
from coding_yusha.controller.core.unit_record import UnitRecord


class Observer():
    allies: list[UnitRecord]
    enemies: list[str]  # 敵の情報は名前のみ
    alive_enemies: list[str]
    past_events: list[EventRecord]

    def __init__(self, allies: list[UnitRecord], enemies: list[str],
                 alive_enemies: list[str]):
        self.allies = allies
        self.enemies = enemies
        self.alive_enemies = alive_enemies
        self.past_events = []

    def get_allies(self) -> list[UnitRecord]:
        return self.allies

    def get_alive_allies(self) -> list[UnitRecord]:
        return [ally for ally in self.allies if ally.current_hp > 0]

    def get_enemies(self) -> list[str]:
        return self.enemies

    def get_alive_enemies(self) -> list[str]:
        return self.alive_enemies

    def get_past_events(self) -> list[EventRecord]:
        return self.past_events

    def update_allies(self, allies):
        self.allies = allies

    def update_enemies(self, enemies):
        self.enemies = enemies

    def update_alive_enemies(self, alive_enemies):
        self.alive_enemies = alive_enemies

    def add_past_event_record(self, event_record: EventRecord):
        self.past_events.append(event_record)
