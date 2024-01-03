import pytest

from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


@pytest.fixture
def ally_01():
    ally_01 = Unit("ally_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    return ally_01


@pytest.fixture
def enemy_01():
    enemy_01 = Unit("enemy_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    return enemy_01


def test_init(ally_01, enemy_01):
    allies = [ally_01]
    enemies = [enemy_01]

    field = Field(allies, enemies)

    assert field.allies == allies
    assert field.enemies == enemies


def test_init_exception_duplicate_unit_name(ally_01, enemy_01):
    ally_02 = Unit("ally_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    allies = [ally_01, ally_02]
    enemies = [enemy_01]

    with pytest.raises(Exception) as e:
        Field(allies, enemies)

    assert str(e.value) == "ユニットの名前が重複しています。"


def test_equals(ally_01, enemy_01):
    allies = [ally_01]
    enemies = [enemy_01]
    field = Field(allies, enemies)
    other = Field(allies, enemies)

    assert field._equals(other)


def test_not_equals(ally_01, enemy_01):
    allies = [ally_01]
    enemies = [enemy_01]
    field = Field(allies, enemies)

    other_ally_01 = Unit("ally_01", 1, 10, 10, 10, 10, 10, 10, 10, 10)
    other_allies = [other_ally_01]
    other = Field(other_allies, enemies)

    assert not field._equals(other)


def test_not_equals_ally_counts(ally_01, enemy_01):
    allies = [ally_01]
    enemies = [enemy_01]
    field = Field(allies, enemies)

    ally_02 = Unit("ally_02", 1, 10, 10, 10, 10, 10, 10, 10, 10)
    other_allies = [ally_01, ally_02]
    other_enemies = [enemy_01]
    other = Field(other_allies, other_enemies)

    assert not field._equals(other)


def test_not_equals_enemy_counts(ally_01, enemy_01):
    allies = [ally_01]
    enemies = [enemy_01]
    field = Field(allies, enemies)

    enemy_02 = Unit("enemy_02", 1, 10, 10, 10, 10, 10, 10, 10, 10)
    other_allies = [ally_01]
    other_enemies = [enemy_01, enemy_02]
    other = Field(other_allies, other_enemies)

    assert not field._equals(other)
