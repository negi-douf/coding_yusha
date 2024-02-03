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


def test_wait_for_next_turn_withdraw(mocker):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    mocker.patch("builtins.input", side_effect=["w"])

    _game_master.wait_for_next_turn()

    assert _game_master.is_buttle_end
    assert _game_master.turn_num == 0


def test_wait_for_next_turn_print_info(mocker, capsys):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    mocker.patch("builtins.input", side_effect=["i"])
    # 事前に入力をクリアしておきたい
    capsys.readouterr()

    _game_master.wait_for_next_turn()
    captured = capsys.readouterr()
    expected = """\
ステージ: test
ターン: 0
enemy_01: HP ?/?, MP ?/?
ally_01: HP 10/10, MP 10/10
ally_02: HP 10/10, MP 10/10

"""

    assert captured.out == expected


def test_wait_for_next_turn_invalid_command(mocker, capsys):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    mocker.patch("builtins.input", side_effect=["invalid_command", "w"])
    # 事前に入力をクリアしておきたい
    capsys.readouterr()

    _game_master.wait_for_next_turn()
    captured = capsys.readouterr()
    expected = "有効なコマンドは ['i', 'w'] です\n"

    assert captured.out == expected
    assert _game_master.is_buttle_end


def test_print_result_withdraw(mocker, capsys):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    mocker.patch("builtins.input", side_effect=["w"])
    # 事前に入力をクリアしておきたい
    capsys.readouterr()

    _game_master.print_result()
    captured = capsys.readouterr()
    expected = """\
撤退した
経過ターン数: 0
"""

    assert captured.out == expected


def test_print_result_victory(capsys):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    _game_master.field.enemies[0].current_hp = 0
    # 事前に入力をクリアしておきたい
    capsys.readouterr()

    _game_master.print_result()
    captured = capsys.readouterr()

    expected = """\
勝利した！
経過ターン数: 0
"""

    assert captured.out == expected


def test_print_result_lose(capsys):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    _game_master.field.allies[0].current_hp = 0
    _game_master.field.allies[1].current_hp = 0
    # 事前に入力をクリアしておきたい
    capsys.readouterr()

    _game_master.print_result()
    captured = capsys.readouterr()

    expected = """\
敗北した...
経過ターン数: 0
"""

    assert captured.out == expected


def test_get_allies_status(game_master):
    expected_ally_01 = Unit()
    expected_ally_01.attach_parameter("coding_yusha/assets/test/ally_01.yml")
    expected_ally_02 = Unit()
    expected_ally_02.attach_parameter("coding_yusha/assets/test/ally_02.yml")

    allies = game_master.get_allies_status()

    assert allies[0]._equals(expected_ally_01)
    assert allies[1]._equals(expected_ally_02)


def test_get_enemies(game_master):
    expected_enemy_01 = Unit()
    expected_enemy_01.attach_parameter("coding_yusha/assets/test/enemy_01.yml")

    enemies = game_master.get_enemies()

    assert enemies[0].name == expected_enemy_01.name
    assert not enemies[0].is_dead()


def test_get_enemies_only_living():
    _game_master = GameMaster("test/an_enemy_is_dead",
                              "coding_yusha/assets/test/an_enemy_is_dead/ally_01.py")

    enemies = _game_master.get_enemies()

    assert len(enemies) == 1


def test_get_enemies_all():
    _game_master = GameMaster("test/an_enemy_is_dead",
                              "coding_yusha/assets/test/an_enemy_is_dead/ally_01.py")

    enemies = _game_master.get_enemies(all_=True)

    assert len(enemies) == 2
    assert enemies[1].is_dead()
