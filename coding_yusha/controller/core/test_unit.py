import pytest

from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.unit import Unit


@pytest.fixture
def sender_unit():
    unit = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    return unit


def test_attack(sender_unit):
    result = sender_unit.attack("target")
    expected_event = Event("sender", "target", "attack")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_special_move(sender_unit):
    result = sender_unit.special_move("target")
    expected_event = Event("sender", "target", "special_move")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_guard(sender_unit):
    result = sender_unit.guard()
    expected_event = Event("sender", "sender", "guard")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_equals(sender_unit):
    other = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    assert sender_unit._equals(other)


def test_not_equals(sender_unit):
    other = Unit("other", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    assert not sender_unit._equals(other)
