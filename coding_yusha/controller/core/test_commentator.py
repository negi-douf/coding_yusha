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
    cmtr.update_allies(allies)
    cmtr.update_enemies(enemies)
    return cmtr


def test_get_allies(commentator):
    allies = commentator.allies
    assert len(allies) == 2
    assert allies[0].name == "ally_01"
    assert allies[1].name == "ally_02"

def test_get_enemies(commentator):
    enemies = commentator.get_enemies()
    assert enemies == ["enemy_01"]
