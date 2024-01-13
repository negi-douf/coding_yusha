import pytest

from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.proceed_event import proceed_event
from coding_yusha.controller.core.unit import Unit


@pytest.fixture
def ally_01():
    ally_01 = Unit()
    ally_01.attach_parameter("coding_yusha/assets/test/ally_01.yml")
    return ally_01


@pytest.fixture
def enemy_01():
    enemy_01 = Unit()
    enemy_01.attach_parameter("coding_yusha/assets/test/enemy_01.yml")
    return enemy_01


def test_proceed_attack(ally_01, enemy_01):
    """
    通常攻撃ダメージ = 攻撃Unitの物理威力 - 防御Unitの物理防御力
    """
    allies = [ally_01]
    enemies = [enemy_01]
    field = Field(allies, enemies)
    event = Event('ally_01', 'enemy_01', 'attack')

    expected_allies = [ally_01]
    expected_enemy_01 = Unit()
    expected_enemy_01.attach_parameter("coding_yusha/assets/test/enemy_01_damaged.yml")
    expected_enemies = [expected_enemy_01]
    expected_field = Field(expected_allies, expected_enemies)

    result_field = proceed_event(event, field)

    assert result_field._equals(expected_field)
