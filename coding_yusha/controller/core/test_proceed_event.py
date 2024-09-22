import pytest

from coding_yusha.controller.core.event import Event
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
    event = Event('ally_01', 'enemy_01', 'attack')
    expected_sender = ally_01
    expected_target = Unit()
    expected_target.attach_parameter("coding_yusha/assets/test/enemy_01_damaged.yml")

    result_sender, result_target = proceed_event(event, ally_01, enemy_01)

    assert result_sender._equals(expected_sender)
    assert result_target._equals(expected_target)


def test_proceed_attack_guarded(ally_01, enemy_01):
    guard_event = Event('enemy_01', 'enemy_01', 'guard')
    attack_event = Event('ally_01', 'enemy_01', 'attack')
    expected_target = Unit()
    expected_target.attach_parameter("coding_yusha/assets/test/enemy_01_guarded.yml")

    guarded_target, _ = proceed_event(guard_event, enemy_01, None)
    result_sender, result_target = proceed_event(attack_event, ally_01, guarded_target)

    assert result_sender._equals(ally_01)
    assert result_target._equals(expected_target)


def test_proceed_guard_event(enemy_01):
    event = Event('enemy_01', 'enemy_01', 'guard')

    result_sender, _ = proceed_event(event, enemy_01, None)

    assert result_sender.is_guarding
    assert result_sender._equals(enemy_01)


def test_proceed_nop_event(ally_01):
    event = Event('ally_01', 'ally_01', 'nop')

    result_sender, _ = proceed_event(event, ally_01, None)

    assert result_sender._equals(ally_01)
