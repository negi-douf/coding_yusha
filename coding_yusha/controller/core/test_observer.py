import pytest

from coding_yusha.controller.core.observer import Observer
from coding_yusha.controller.core.unit_record import UnitRecord

# テストしたいこと
# ユニットの行動を返せるか
# 味方の情報を返せるか
# 敵の一覧を返せるか
# 生きている敵の一覧を返せるか


@pytest.fixture
def observer():
    obsr = Observer()
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
    obsr.update_all_allies(allies)
    obsr.update_alive_allies(allies)
    obsr.update_all_enemies(enemies)
    return obsr


def test_get_all_allies(observer):
    allies = observer.get_all_allies()
    assert len(allies) == 2
    assert allies[0].name == "ally_01"
    assert allies[1].name == "ally_02"


def test_get_all_enemies(observer):
    enemies = observer.get_all_enemies()
    assert len(enemies) == 1
    assert enemies[0] == "enemy_01"


def test_update_all_allies(observer):
    new_allies = [
        UnitRecord(
            name="ally_03",
            max_hp=10,
            current_hp=10,
            max_mp=10,
            current_mp=10
        )
    ]
    observer.update_all_allies(new_allies)
    allies = observer.get_all_allies()
    assert len(allies) == 1
    assert allies[0].name == "ally_03"


def test_update_all_enemies(observer):
    new_enemies = ["enemy_02", "enemy_03"]
    observer.update_all_enemies(new_enemies)
    enemies = observer.get_all_enemies()
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
    observer.update_all_allies([ally_alive, ally_dead])
    observer.update_alive_allies([ally_alive])
    alive_allies = observer.get_alive_allies()
    assert len(alive_allies) == 1
    assert alive_allies[0].name == "ally_alive"


def test_get_alive_enemies(observer):
    observer.update_all_enemies(["enemy_01", "enemy_02"])
    observer.update_alive_enemies(["enemy_01"])
    alive_enemies = observer.get_alive_enemies()
    assert len(alive_enemies) == 1
    assert alive_enemies[0] == "enemy_01"
