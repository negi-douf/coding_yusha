import pytest

from coding_yusha.controller.core import initialize_field


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
