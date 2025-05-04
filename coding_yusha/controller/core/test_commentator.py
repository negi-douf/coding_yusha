import pytest

from coding_yusha.controller.core.commentator import Commentator
from coding_yusha.controller.core.unit_record import UnitRecord

# テストしたいこと
# ユニットの行動を返せるか
# 味方の情報を返せるか
# 敵の一覧を返せるか
# 生きている敵の一覧を返せるか

@pytest.fixture
def commentator():
    cmtr = Commentator()
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
    cmtr.update_all_allies(allies)
    cmtr.update_alive_allies(allies)
    cmtr.update_all_enemies(enemies)
    return cmtr


def test_get_all_allies(commentator):
    allies = commentator.get_all_allies()
    assert len(allies) == 2
    assert allies[0].name == "ally_01"
    assert allies[1].name == "ally_02"


def test_get_all_enemies(commentator):
    enemies = commentator.get_all_enemies()
    assert len(enemies) == 1
    assert enemies[0] == "enemy_01"


def test_update_all_allies(commentator):
    new_allies = [
        UnitRecord(
            name="ally_03",
            max_hp=10,
            current_hp=10,
            max_mp=10,
            current_mp=10
        )
    ]
    commentator.update_all_allies(new_allies)
    allies = commentator.get_all_allies()
    assert len(allies) == 1
    assert allies[0].name == "ally_03"


def test_update_all_enemies(commentator):
    new_enemies = ["enemy_02", "enemy_03"]
    commentator.update_all_enemies(new_enemies)
    enemies = commentator.get_all_enemies()
    assert len(enemies) == 2
    assert enemies[0] == "enemy_02"
    assert enemies[1] == "enemy_03"


def test_get_alive_allies(commentator):
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
    commentator.update_all_allies([ally_alive, ally_dead])
    commentator.update_alive_allies([ally_alive])
    alive_allies = commentator.get_alive_allies()
    assert len(alive_allies) == 1
    assert alive_allies[0].name == "ally_alive"
