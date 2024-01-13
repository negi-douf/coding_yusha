from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit
from coding_yusha.controller.game_master import GameMaster


def test_init():
    game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                             "coding_yusha/assets/test/ally_02.py")
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
    expected_ally_files = {
        "ally_01": {
            "yml": "coding_yusha/assets/test/ally_01.yml",
            "py": "coding_yusha/assets/test/ally_01.py",
        },
        "ally_02": {
            "yml": "coding_yusha/assets/test/ally_02.yml",
            "py": "coding_yusha/assets/test/ally_02.py",
        },
    }
    expected_enemy_files = {
        "enemy_01": {
            "yml": "coding_yusha/assets/test/enemy_01.yml",
            "py": "coding_yusha/assets/test/enemy_01.py",
        },
    }
    expected_field = Field([expected_ally_01, expected_ally_02], [expected_enemy_01])

    assert game_master.stage_info == expected_stage_info
    assert game_master.ally_files == expected_ally_files
    assert game_master.enemy_files == expected_enemy_files
    assert game_master.field._equals(expected_field)
