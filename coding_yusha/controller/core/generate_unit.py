from coding_yusha.controller.core.unit import Unit


def generate_allies(ally_file_map: dict[str, str]) -> list[Unit]:
    # NOTE: mapから作るのが最適なのだろうか
    allies = []
    for ally in ally_file_map:
        _ally = generate_unit_from_py(ally_file_map[ally]["py"], ally_file_map[ally]["yml"])
        _ally.attach_parameter(ally_file_map[ally]["yml"])
        allies.append(_ally)
    return allies


def generate_enemies(enemy_file_map: dict[str, str]) -> list[Unit]:
    enemies = []
    for enemy in enemy_file_map:
        _enemy = Unit()
        _enemy.attach_parameter(enemy_file_map[enemy]["yml"])
        enemies.append(_enemy)
    return enemies


def generate_unit_from_py(unit_py: str, unit_yml: str) -> Unit:
    """
    pyファイルから Unitを生成する
    プレイヤーの定義した振る舞いをさせるために、
    pyファイルの文字列を読み込んで、execで実行する
    """
    with open(unit_py, "r", encoding="utf-8") as f:
        code = f.read()
    global main
    exec(code, globals())
    result = {}
    try:
        exec("unit = main()", globals(), result)
        unit = result["unit"]
        unit.attach_parameter(unit_yml)
        return unit
    except Exception as e:
        original_error_str = f"{e.__class__.__name__}: {str(e)}"

    # TODO: 専用のエラークラスを作る
    # TODO: 呼び出し元で余計なスタックトレースを表示しないようにする
    raise Exception(
        f"Unitの生成に失敗しました: {unit_py}\n"
        + "指定された pyファイルで以下のエラーが発生しました\n"
        + original_error_str)
