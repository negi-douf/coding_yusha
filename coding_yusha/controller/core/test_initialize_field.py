import pytest
from yaml import safe_load

from coding_yusha.controller.core import initialize_field
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


@pytest.fixture
def test_stage_info():
    stage_info = {
        "allies": ["ally_01.yml", "ally_02.yml"],
        "enemies": ["enemy_01.yml"],
    }
    return stage_info


def test_load_stage_info():
    expected = {
        "stage": "test",
        "dir": "coding_yusha/assets/test",
        "allies": ["ally_01.yml", "ally_02.yml"],
        "enemies": ["enemy_01.yml"],
    }

    result = initialize_field.load_stage_info("test")

    assert result == expected


def test_load_stage_info_not_found():
    with pytest.raises(FileNotFoundError) as e:
        _ = initialize_field.load_stage_info("test/not_found")

    assert str(e.value) == "infoファイルが見つかりません: test/not_found"


def test_validate_stage_info_allies_key_not_found():
    with open("coding_yusha/assets/test/allies_key_not_found/info.yml", "r") as f:
        stage_info = safe_load(f)
    with pytest.raises(KeyError) as e:
        assert initialize_field.validate_stage_info("test/allies_key_not_found", stage_info)

    assert str(e.value) == "\"infoファイルの中に 'allies'が見つかりません\""


def test_validate_stage_info_enemies_key_not_found():
    with open("coding_yusha/assets/test/enemies_key_not_found/info.yml", "r") as f:
        stage_info = safe_load(f)
    with pytest.raises(KeyError) as e:
        assert initialize_field.validate_stage_info("test/enemies_key_not_found", stage_info)

    assert str(e.value) == "\"infoファイルの中に 'enemies'が見つかりません\""


def test_validate_stage_info_enemy_yml_not_found():
    with open("coding_yusha/assets/test/enemy_yml_not_found/info.yml", "r") as f:
        stage_info = safe_load(f)
    with pytest.raises(FileNotFoundError) as e:
        assert initialize_field.validate_stage_info("test/enemy_yml_not_found", stage_info)

    assert str(e.value) == "敵の ymlファイルが見つかりません: enemy_01.yml"


def test_validate_stage_info_enemy_py_not_found():
    with open("coding_yusha/assets/test/enemy_py_not_found/info.yml", "r") as f:
        stage_info = safe_load(f)
    with pytest.raises(FileNotFoundError) as e:
        assert initialize_field.validate_stage_info("test/enemy_py_not_found", stage_info)

    assert str(e.value) == "敵の ymlファイルが見つかりません: enemy_01.yml"


def test_validate_stage_info_ally_yml_not_found():
    with open("coding_yusha/assets/test/ally_yml_not_found/info.yml", "r") as f:
        stage_info = safe_load(f)
    with pytest.raises(FileNotFoundError) as e:
        assert initialize_field.validate_stage_info("test/ally_yml_not_found", stage_info)

    assert str(e.value) == "味方の ymlファイルが見つかりません: ally_02.yml"


def test_validate_ally_py_files(test_stage_info):
    ally_py_files = ["ally_01.py", "ally_02.py"]

    assert initialize_field.validate_ally_py_files(test_stage_info, ally_py_files)


def test_validate_ally_py_files_not_enough(test_stage_info):
    ally_py_files = ["ally_01.py"]

    with pytest.raises(FileNotFoundError) as e:
        initialize_field.validate_ally_py_files(test_stage_info, ally_py_files)

    assert str(e.value) == "味方の pyファイルの数が不正です"


def test_validate_ally_py_files_name_unmatch(test_stage_info):
    ally_py_files = ["ally_01.py", "ally_03.py"]

    with pytest.raises(FileNotFoundError) as e:
        initialize_field.validate_ally_py_files(test_stage_info, ally_py_files)

    assert str(e.value) == "味方の pyファイルの名前が不正です: ally_03"


def test_initialize_field():
    ally_py_files = ["coding_yusha/assets/test/ally_01.py",
                     "coding_yusha/assets/test/ally_02.py"]
    ally_01 = Unit()
    ally_01.attach_parameter("coding_yusha/assets/test/ally_01.yml")
    ally_02 = Unit()
    ally_02.attach_parameter("coding_yusha/assets/test/ally_02.yml")
    enemy_01 = Unit()
    enemy_01.attach_parameter("coding_yusha/assets/test/enemy_01.yml")
    stage_info = {
        "stage": "test",
        "dir": "coding_yusha/assets/test",
        "allies": ["ally_01.yml", "ally_02.yml"],
        "enemies": ["enemy_01.yml"],
    }
    expected_field = Field([ally_01, ally_02], [enemy_01])

    field = initialize_field.initialize_field(stage_info, ally_py_files)

    assert field._equals(expected_field)
