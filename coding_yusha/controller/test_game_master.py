import pytest

from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit
from coding_yusha.controller.game_master import GameMaster


@pytest.fixture
def game_master():
    return GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                      "coding_yusha/assets/test/ally_02.py")


def test_init(game_master):
    expected_ally_01 = Unit()
    expected_ally_01.attach_parameter("coding_yusha/assets/test/ally_01.yml")
    expected_ally_02 = Unit()
    expected_ally_02.attach_parameter("coding_yusha/assets/test/ally_02.yml")
    expected_enemy_01 = Unit()
    expected_enemy_01.attach_parameter("coding_yusha/assets/test/enemy_01.yml")
    expected_stage_info = {
        "stage": "test",
        "dir": "coding_yusha/assets/test",
        "allies": ["ally_01.yml", "ally_02.yml"],
        "enemies": ["enemy_01.yml"],
    }
    expected_ally_file_map = {
        "ally_01": {
            "yml": "coding_yusha/assets/test/ally_01.yml",
            "py": "coding_yusha/assets/test/ally_01.py",
        },
        "ally_02": {
            "yml": "coding_yusha/assets/test/ally_02.yml",
            "py": "coding_yusha/assets/test/ally_02.py",
        },
    }
    expected_enemy_file_map = {
        "enemy_01": {
            "yml": "coding_yusha/assets/test/enemy_01.yml",
            "py": "coding_yusha/assets/test/enemy_01.py",
        },
    }
    expected_field = Field([expected_ally_01, expected_ally_02], [expected_enemy_01])

    assert game_master.stage_info == expected_stage_info
    assert game_master.ally_file_map == expected_ally_file_map
    assert game_master.enemy_file_map == expected_enemy_file_map
    assert game_master.field._equals(expected_field)


def test_decide_action_order(game_master):
    units_ordered = game_master.decide_action_order()

    # 素早さが同じ場合はランダムに並ぶ
    # ally_01と enemy_01 の素早さは同じであるため、末尾だけを確認する
    assert units_ordered[2].name == "ally_02"


def test_print_stage_info(game_master, capsys):
    game_master.print_stage_info()
    captured = capsys.readouterr()
    expected = """\
【戦闘開始】
ステージ: test
敵: ['enemy_01']
味方: ['ally_01', 'ally_02']
"""

    assert captured.out == expected


def test_wait_for_next_turn_withdraw(game_master, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "w")

    game_master.wait_for_next_turn()

    assert game_master.is_buttle_end
    assert game_master.turn_num == 0
