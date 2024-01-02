from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.unit import Unit


def test_attack():
    unit = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    result = unit.attack("target")

    assert result == Event("sender", "target", "attack")


def test_special_move():
    unit = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    result = unit.special_move("target")

    assert result == Event("sender", "target", "special_move")


def test_guard():
    unit = Unit("sender", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    result = unit.guard()

    assert result == Event("sender", "sender", "guard")
