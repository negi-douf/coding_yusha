import pytest

from coding_yusha.controller.core.unit import Unit


def test_create_unit_from_yml():
    unit = create_unit_from_yml("test", "success.yml")
    expected_unit = Unit("unit", 10, 10, 10, 10, 10, 10, 10, 10, 10)

    assert unit._equals(expected_unit)


def test_create_unit_from_yml_parameter_not_enough():
    with pytest.raises(Exception) as e:
        create_unit_from_yml("test", "not_enough.yml")

    assert str(e.value) == "Unitの初期化に必要なパラメータが不足しています。"


def test_create_unit_from_yml_not_found():
    with pytest.raises(Exception) as e:
        create_unit_from_yml("test", "not_found.yml")

    assert str(e.value) == "ファイルが見つかりません。"
