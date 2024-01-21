import pytest

from coding_yusha.controller.core.field import Field
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


@pytest.fixture
def field_01(ally_01, enemy_01):
    allies = [ally_01]
    enemies = [enemy_01]
    return Field(allies, enemies)


def test_init(ally_01, enemy_01, field_01):
    allies = [ally_01]
    enemies = [enemy_01]
    assert field_01.allies == allies
    assert field_01.enemies == enemies


def test_init_exception_duplicate_unit_name(ally_01, enemy_01):
    ally_02 = Unit()
    ally_02.attach_parameter("coding_yusha/assets/test/ally_01.yml")
    allies = [ally_01, ally_02]
    enemies = [enemy_01]

    with pytest.raises(Exception) as e:
        Field(allies, enemies)

    assert str(e.value) == "ユニットの名前が重複しています。"


# def test_is_buttle_end_enemies_dead(field_01):
#     assert not field_01.is_buttle_end()
#     field_01.enemies[0].current_hp = 0

#     assert field_01.is_buttle_end()


# def test_is_buttle_end_allies_dead(ally_01, enemy_01):
#     ally_02 = Unit()
#     ally_02.attach_parameter("coding_yusha/assets/test/ally_02.yml")
#     field = Field([ally_01, ally_02], [enemy_01])

#     assert not field.is_buttle_end()
#     field.allies[0].current_hp = 0
#     assert not field.is_buttle_end()
#     field.allies[1].current_hp = 0

#     assert field.is_buttle_end()


def test_equals(ally_01, enemy_01, field_01):
    allies = [ally_01]
    enemies = [enemy_01]
    other = Field(allies, enemies)

    assert other._equals(field_01)


def test_not_equals(enemy_01, field_01):
    enemies = [enemy_01]
    ally_02 = Unit()
    ally_02.attach_parameter("coding_yusha/assets/test/ally_02.yml")
    other_allies = [ally_02]
    other = Field(other_allies, enemies)

    assert not other._equals(field_01)


def test_not_equals_ally_count(ally_01, enemy_01, field_01):
    ally_02 = Unit()
    ally_02.attach_parameter("coding_yusha/assets/test/ally_02.yml")
    other_allies = [ally_01, ally_02]
    other_enemies = [enemy_01]
    other = Field(other_allies, other_enemies)

    assert not other._equals(field_01)


def test_not_equals_enemy_count(ally_01, enemy_01):
    allies = [ally_01]
    enemies = [enemy_01]
    field = Field(allies, enemies)

    enemy_02 = Unit()
    enemy_02.attach_parameter("coding_yusha/assets/test/ally_02.yml")
    other_allies = [ally_01]
    other_enemies = [enemy_01, enemy_02]
    other = Field(other_allies, other_enemies)

    assert not field._equals(other)
