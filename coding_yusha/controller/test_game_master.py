import pytest

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

    assert game_master.stage_info == expected_stage_info
    assert game_master.ally_file_map == expected_ally_file_map
    assert game_master.enemy_file_map == expected_enemy_file_map


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


def test_is_battle_end_withdraw(game_master):
    assert not game_master.is_battle_end()

    game_master.withdraw = True

    assert game_master.is_battle_end()


def test_is_battle_end_won(game_master):
    assert not game_master.is_battle_end()

    game_master.lost = False
    game_master.won = True

    assert game_master.is_battle_end()


def test_is_battle_end_lost(game_master):
    assert not game_master.is_battle_end()

    game_master.withdraw = False
    game_master.lost = True

    assert game_master.is_battle_end()


def test_update_battle_status_neutral(game_master):
    game_master.update_battle_status()

    assert not game_master.won
    assert not game_master.lost


def test_update_battle_status_won():
    _game_master = GameMaster("test/enemies_dead",
                              "coding_yusha/assets/test/enemies_dead/ally_01.py")

    _game_master.update_battle_status()

    assert _game_master.won


def test_update_battle_status_lost():
    _game_master = GameMaster("test/allies_dead",
                              "coding_yusha/assets/test/allies_dead/ally_dead.py")

    _game_master.update_battle_status()

    assert _game_master.lost


def test_decide_action_order(game_master):
    units_ordered = game_master.decide_action_order()

    # 素早さが同じ場合はランダムに並ぶ
    # ally_01と enemy_01 の素早さは同じであるため、末尾だけを確認する
    assert units_ordered[2].name == "ally_02"


def test_wait_for_next_turn_battle(mocker, capsys):
    # テスト用のステージをもうひとつ作ったほうがいいかも
    _game_master = GameMaster("test/battle", "coding_yusha/assets/test/battle/attacker.py")
    mocker.patch("builtins.input", side_effect=["b"])
    # 事前に入力をクリアしておきたい
    capsys.readouterr()

    _game_master.wait_for_next_turn()
    captured = capsys.readouterr()
    expected = """\
ターン: 0
attacker の攻撃！
nop に 5 のダメージ！
nop はじっとしている

"""

    assert captured.out == expected


def test_wait_for_next_turn_battle_defeat(mocker, capsys):
    _game_master = GameMaster("test/battle", "coding_yusha/assets/test/battle/attacker.py")
    mocker.patch("builtins.input", side_effect=["b", "b"])
    _game_master.wait_for_next_turn()
    # 事前に入力をクリアしておきたい
    capsys.readouterr()

    _game_master.wait_for_next_turn()
    captured = capsys.readouterr()
    expected = """\
ターン: 1
attacker の攻撃！
nop に 5 のダメージ！
nop は倒れた

"""

    assert captured.out == expected


def test_wait_for_next_turn_withdraw(mocker):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    mocker.patch("builtins.input", side_effect=["w"])

    _game_master.wait_for_next_turn()

    assert _game_master.withdraw
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
    expected = "有効なコマンドは ['b', 'i', 'w'] です\n"

    assert captured.out == expected


def test_reset_units():
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    _game_master.allies[0].is_guarding = True
    _game_master.enemies[0].is_guarding = True

    _game_master.reset_units()

    assert not _game_master.allies[0].is_guarding
    assert not _game_master.enemies[0].is_guarding


def test_proceed_battle(mocker):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    mocker.patch("coding_yusha.controller.game_master.GameMaster.decide_action_order",
                 return_value=_game_master.allies + _game_master.enemies)
    proceed_event_mock = mocker.patch("coding_yusha.controller.game_master.proceed_event")

    _game_master.proceed_battle()

    assert proceed_event_mock.call_count == 3
    assert _game_master.turn_num == 1


def test_proceed_battle_an_ally_is_dead(mocker):
    _game_master = GameMaster("test/an_ally_is_dead",
                              "coding_yusha/assets/test/an_ally_is_dead/ally_01.py",
                              "coding_yusha/assets/test/an_ally_is_dead/ally_dead.py")
    mocker.patch("coding_yusha.controller.game_master.GameMaster.decide_action_order",
                 return_value=_game_master.allies + _game_master.enemies)
    proceed_event_mock = mocker.patch("coding_yusha.controller.game_master.proceed_event")

    _game_master.proceed_battle()

    assert proceed_event_mock.call_count == 2
    assert len(_game_master.allies) + len(_game_master.enemies) == 3
    assert _game_master.turn_num == 1


def test_proceed_battle_an_enemy_is_dead(mocker):
    _game_master = GameMaster("test/an_enemy_is_dead",
                              "coding_yusha/assets/test/an_enemy_is_dead/ally_01.py")
    mocker.patch("coding_yusha.controller.game_master.GameMaster.decide_action_order",
                 return_value=_game_master.allies + _game_master.enemies)
    proceed_event_mock = mocker.patch("coding_yusha.controller.game_master.proceed_event")

    _game_master.proceed_battle()

    assert proceed_event_mock.call_count == 2
    assert len(_game_master.allies) + len(_game_master.enemies) == 3
    assert _game_master.turn_num == 1


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


def test_print_result_win(capsys):
    _game_master = GameMaster("test", "coding_yusha/assets/test/ally_01.py",
                              "coding_yusha/assets/test/ally_02.py")
    _game_master.enemies[0].current_hp = 0
    _game_master.won = True
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
    _game_master.allies[0].current_hp = 0
    _game_master.allies[1].current_hp = 0
    _game_master.lost = True
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
