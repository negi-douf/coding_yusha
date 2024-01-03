import pytest

from coding_yusha.controller.core.create_unit_from_yml import create_unit_from_yml
from coding_yusha.controller.core.unit import Unit


def test_create_unit_from_yml():
    unit = create_unit_from_yml("test", "ally_01.yml")
    expected_unit = Unit("ally_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    assert unit._equals(expected_unit)


def test_create_unit_from_yml_parameter_not_enough():
    with pytest.raises(KeyError) as e:
        create_unit_from_yml("test", "not_enough.yml")

    assert str(e.value) == "'Unitの初期化に必要なパラメータが見つかりません。'"


def test_create_unit_from_yml_not_found():
    with pytest.raises(FileNotFoundError) as e:
        create_unit_from_yml("test", "not_found.yml")

    assert str(e.value) == "ファイルが見つかりません。"
