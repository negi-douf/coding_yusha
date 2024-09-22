from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.unit import Unit


def proceed_event(event: Event, sender: Unit, target: Unit) -> tuple[Unit, Unit]:
    """
    取得したイベントを元にフィールドを処理する

    Args:
        event (Event): イベント
        sender (Unit): イベントを発生させたユニット
        target (Unit): イベントの対象ユニット

    Returns:
        tuple[Unit, Unit]: 処理後のユニット
    """
    if event.move == "attack":
        return _proceed_attack(sender, target)
    # elif event.move == "special_move":
    elif event.move == "guard":
        return _proceed_guard(sender), target
    elif event.move == "nop":
        return _proceed_nop(sender), target
    else:
        raise Exception("不正なイベントです。処理可能event.moveは\"attack\" \"special_move\" \"guard\"です。")


def _proceed_attack(sender: Unit, target: Unit) -> tuple[Unit, Unit]:
    """
    通常攻撃イベントを処理する

    Args:
        sender (Unit): 攻撃側ユニット
        target (Unit): 被攻撃側ユニット

    Returns:
        tuple[Unit, Unit]: 処理後のユニット
    """
    if sender.is_dead():
        return sender, target
    print(f"{sender.name} の攻撃！")
    damage = _calculate_damage(sender, target)
    target.current_hp -= damage
    print(f"{target.name} に {damage} のダメージ！")
    if target.current_hp <= 0:
        target.current_hp = 0
        print(f"{target.name} は倒れた")
    return sender, target


def _proceed_guard(sender: Unit) -> Unit:
    """
    防御イベントを処理する

    Args:
        sender (Unit): 対象ユニット

    Returns:
        tuple[Unit, Unit]: 処理後のユニット
    """
    sender.is_guarding = True
    return sender


def _proceed_nop(sender: Unit) -> Unit:
    """
    何もしないイベントを処理する

    Args:
        sender (Unit): 対象ユニット

    Returns:
        Unit: 処理後のユニット
    """
    if not sender.is_dead():
        print(f"{sender.name} はじっとしている")
    return sender


def _calculate_damage(sender: Unit, target: Unit) -> int:
    """
    Eventによって発生するHP増減値を計算する

    Args:
        sender (Unit): 攻撃側ユニット
        target (Unit): 被攻撃側ユニット

    Returns:
        int: HP増減値
    """
    if sender.pa - target.pd < 0:
        return 0
    elif target.is_guarding:
        return (sender.pa - target.pd) // 2
    return sender.pa - target.pd
