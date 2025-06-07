import pytest

from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.observer import Observer
from coding_yusha.controller.core.unit_record import UnitRecord

# テストしたいこと
# ユニットの行動を返せるか
# 味方の情報を返せるか
# 敵の一覧を返せるか
# 生きている敵の一覧を返せるか


@pytest.fixture
def observer():
    ally_01 = UnitRecord(
        name="ally_01",
        max_hp=10,
        current_hp=10,
        max_mp=10,
        current_mp=10
    )
    ally_02 = UnitRecord(
        name="ally_02",
        max_hp=10,
        current_hp=10,
        max_mp=10,
        current_mp=10
    )
    allies = [ally_01, ally_02]
    enemies = ["enemy_01"]
    obsr = Observer(allies, enemies, enemies)
    return obsr


def test_get_allies(observer):
    allies = observer.get_allies()
    assert len(allies) == 2
    assert allies[0].name == "ally_01"
    assert allies[1].name == "ally_02"


def test_get_enemies(observer):
    enemies = observer.get_enemies()
    assert len(enemies) == 1
    assert enemies[0] == "enemy_01"


def test_update_allies(observer):
    new_allies = [
        UnitRecord(
            name="ally_03",
            max_hp=10,
            current_hp=10,
            max_mp=10,
            current_mp=10
        )
    ]
    observer.update_allies(new_allies)
    allies = observer.get_allies()
    assert len(allies) == 1
    assert allies[0].name == "ally_03"


def test_update_enemies(observer):
    new_enemies = ["enemy_02", "enemy_03"]
    observer.update_enemies(new_enemies)
    enemies = observer.get_enemies()
    assert len(enemies) == 2
    assert enemies[0] == "enemy_02"
    assert enemies[1] == "enemy_03"


def test_get_alive_allies(observer):
    ally_alive = UnitRecord(
        name="ally_alive",
        max_hp=10,
        current_hp=10,
        max_mp=10,
        current_mp=10
    )
    ally_dead = UnitRecord(
        name="ally_dead",
        max_hp=10,
        current_hp=0,
        max_mp=10,
        current_mp=10
    )
    observer.update_allies([ally_alive, ally_dead])
    alive_allies = observer.get_alive_allies()
    assert len(alive_allies) == 1
    assert alive_allies[0].name == "ally_alive"


def test_get_alive_enemies(observer):
    observer.update_enemies(["enemy_01", "enemy_02"])
    alive_enemies = observer.get_alive_enemies()
    assert len(alive_enemies) == 1
    assert alive_enemies[0] == "enemy_01"


def test_get_past_events_empty(observer):
    empty_events = observer.get_past_events()
    assert len(empty_events) == 0


def test_add_past_event(observer):
    event = Event(sender="ally_01", target="enemy_01", move="attack")
    observer.add_past_event(event)
    past_events = observer.get_past_events()
    assert len(past_events) == 1
    assert past_events[0].sender == "ally_01"
    assert past_events[0].target == "enemy_01"
    assert past_events[0].move == "attack"
