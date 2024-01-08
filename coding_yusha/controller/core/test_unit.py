import pytest

from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.unit import Unit


@pytest.fixture
def ally_01():
    unit = Unit("test", "ally_01.yml")
    return unit


def test_attack(ally_01):
    result = ally_01.attack("target")
    expected_event = Event("ally_01", "target", "attack")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_special_move(ally_01):
    result = ally_01.special_move("target")
    expected_event = Event("ally_01", "target", "special_move")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_guard(ally_01):
    result = ally_01.guard()
    expected_event = Event("ally_01", "ally_01", "guard")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_equals(ally_01):
    other = Unit("test", "ally_01.yml")

    assert ally_01._equals(other)


def test_not_equals(ally_01):
    other = Unit("test", "ally_02.yml")

    assert not ally_01._equals(other)


def test_init_yml_not_found():
    with pytest.raises(FileNotFoundError) as e:
        Unit("test", "not_found.yml")

    assert str(e.value) == "ymlファイルが見つかりません: coding_yusha/assets/test/not_found.yml"


def test_init_parameter_not_enough():
    with pytest.raises(KeyError) as e:
        Unit("test", "not_enough.yml")

    assert str(e.value) == "'Unitの初期化に必要なパラメータが見つかりません: coding_yusha/assets/test/not_enough.yml'"
