import pytest

from coding_yusha.controller.core import initialize_field


@pytest.fixture
def test_stage_info():
    stage_info = {
        "allies": ["ally_01.yml", "ally_02.yml"],
        "enemies": ["enemy_01.yml"],
    }
    return stage_info


def test_load_stage_info():
    expected = {
        "allies": ["ally_01.yml", "ally_02.yml"],
        "enemies": ["enemy_01.yml"],
    }

    result = initialize_field.load_stage_info("test")

    assert result == expected


def test_load_stage_info_not_found():
    with pytest.raises(FileNotFoundError) as e:
        _ = initialize_field.load_stage_info("test/not_found")

    assert str(e.value) == "infoファイルが見つかりません: test/not_found"


def test_load_stage_info_allies_not_found():
    with pytest.raises(KeyError) as e:
        _ = initialize_field.load_stage_info("test/allies_not_found")

    assert str(e.value) == "\"infoファイルの中に 'allies'が見つかりません\""


def test_load_stage_info_enemies_not_found():
    with pytest.raises(KeyError) as e:
        _ = initialize_field.load_stage_info("test/enemies_not_found")

    assert str(e.value) == "\"infoファイルの中に 'enemies'が見つかりません\""


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
