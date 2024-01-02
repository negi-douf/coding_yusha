from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.unit import Unit


def test_attack():
    unit = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    result = unit.attack("target")
    expected_event = Event("sender", "target", "attack")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_special_move():
    unit = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    result = unit.special_move("target")
    expected_event = Event("sender", "target", "special_move")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move


def test_guard():
    unit = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    result = unit.guard()
    expected_event = Event("sender", "sender", "guard")

    assert result.sender == expected_event.sender
    assert result.target == expected_event.target
    assert result.move == expected_event.move
