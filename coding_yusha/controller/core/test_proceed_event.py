from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.proceed_event import proceed_event
from coding_yusha.controller.core.unit import Unit


def test_proceed_attack():
    """
    通常攻撃ダメージ = 攻撃Unitの物理威力 - 防御Unitの物理防御力
    """
    ally_01 = Unit("ally_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    allies = [ally_01]
    enemy_01 = Unit("enemy_01", 10, 10, 10, 10, 10, 5, 10, 10, 10)
    enemies = [enemy_01]
    field = Field(allies, enemies)
    event = Event('ally_01', 'enemy_01', 'attack')

    expected_ally_01 = Unit("ally_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    expected_allies = [expected_ally_01]
    expected_enemy_01 = Unit("enemy_01", 10, 5, 10, 10, 10, 5, 10, 10, 10)
    expected_enemies = [expected_enemy_01]
    expected_field = Field(expected_allies, expected_enemies)

    result_field = proceed_event(event, field)

    assert result_field._equals(expected_field)
