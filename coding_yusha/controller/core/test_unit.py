import pytest

from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.unit import Unit


@pytest.fixture
def ally_01():
    unit = Unit()
    unit.attach_parameter("coding_yusha/assets/test/ally_01.yml")
    return unit


def test_attach_parameter(ally_01):
    assert ally_01.name == "ally_01"
    assert ally_01.max_hp == 10
    assert ally_01.current_hp == 10
    assert ally_01.max_mp == 10
    assert ally_01.current_mp == 10
    assert ally_01.pa == 10
    assert ally_01.pd == 10
    assert ally_01.ma == 10
    assert ally_01.md == 10
    assert ally_01.agi == 10


def test_is_dead(ally_01):
    assert not ally_01.is_dead()
    ally_01.current_hp = 0

    assert ally_01.is_dead()


def test_reset_status(ally_01):
    ally_01.is_guarding = True
    ally_01.reset_status()

    assert not ally_01.is_guarding


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
    other = Unit()
    other.name = "ally_01"
    other.max_hp = 10
    other.current_hp = 10
    other.max_mp = 10
    other.current_mp = 10
    other.pa = 10
    other.pd = 10
    other.ma = 10
    other.md = 10
    other.agi = 10

    assert ally_01._equals(other)


def test_not_equals(ally_01):
    other = Unit()
    other.attach_parameter("coding_yusha/assets/test/ally_02.yml")

    assert not ally_01._equals(other)


def test_init_yml_not_found():
    unit = Unit()
    with pytest.raises(FileNotFoundError) as e:
        unit.attach_parameter("coding_yusha/assets/test/not_found.yml")

    assert str(e.value) == "ymlファイルが見つかりません: coding_yusha/assets/test/not_found.yml"


def test_init_parameter_not_enough():
    unit = Unit()
    with pytest.raises(KeyError) as e:
        unit.attach_parameter("coding_yusha/assets/test/not_enough.yml")

    assert str(e.value) == "'Unitの初期化に必要なパラメータが見つかりません: coding_yusha/assets/test/not_enough.yml'"
