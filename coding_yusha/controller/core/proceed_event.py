from coding_yusha.controller.core.event import Event
from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


def proceed_event(event: Event, field: Field) -> Field:
    """
    取得したイベントを元にフィールドを処理する

    Args:
        event (Event): イベント
        field (Field): フィールド

    Returns:
        Field: 処理後のフィールド
    """
    if event.move == "attack":
        return _proceed_attack(event, field)
    # elif event.move == "special_move":
    #     return _proceed_special_move(event, field)
    elif event.move == "guard":
        return _proceed_guard(event, field)
    else:
        raise Exception("不正なイベントです。処理可能event.moveは\"attack\" \"special_move\" \"guard\"です。")


def _proceed_attack(event: Event, field: Field) -> Field:
    """
    通常攻撃イベントを処理する

    Args:
        event (Event): 通常攻撃イベント
        field (Field): フィールド

    Returns:
        Field: 処理後のフィールド
    """
    sender = _get_unit(event.sender, field)
    target = _get_unit(event.target, field)
    damage = _calculate_damage(sender, target)
    target.current_hp -= damage
    return field


def _proceed_guard(event: Event, field: Field) -> Field:
    """
    防御イベントを処理する

    Args:
        event (Event): 防御イベント
        field (Field): フィールド

    Returns:
        Field: 処理後のフィールド
    """
    target = _get_unit(event.target, field)
    target.is_guarding = True
    return field


def _get_unit(name: str, field: Field) -> Unit:
    """
    フィールドに存在するUnitから、指定した名前と一致するUnitインスタンスを取得する

    Args:
        name (str): ユニット名
        field (Field): フィールド

    Returns:
        Unit: Unitインスタンス
    """
    for ally in field.allies:
        if ally.name == name:
            return ally
    for enemy in field.enemies:
        if enemy.name == name:
            return enemy
    raise Exception(f"{name}と一致するUnitが見つかりません")


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
