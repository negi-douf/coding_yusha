from os import path

from yaml import safe_load

from coding_yusha.controller.core.field import Field
from coding_yusha.controller.core.unit import Unit


def initialize_field(stage: str, ally_py_files: list[str]):
    stage_info = load_stage_info(stage)
    validate_ally_py_files(stage_info, ally_py_files)
    files_map = map_files(stage, stage_info, ally_py_files)
    allies = []
    for ally_py in ally_py_files:
        allies.append(generate_unit_from_py(ally_py))
    (allies, enemies) = initialize_units(stage, files_map)
    field = Field(allies, enemies)
    return field


def load_stage_info(stage: str):
    default_yml_dir = "coding_yusha/assets"
    info_yml_path = path.join(default_yml_dir, stage, "info.yml")
    try:
        with open(info_yml_path, "r", encoding="utf-8") as f:
            body = safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"infoファイルが見つかりません: {stage}") from e

    validate_stage_info(stage, body)
    return body


def validate_stage_info(stage: str, stage_info: dict[str, list[str]]):
    """
        確認したいのは
        1. dictの中に alliesの keyが存在すること
        2. dictの中に enemiesの keyが存在すること
        3. enemiesの ymlが存在すること
        4. enemiesの pyが存在すること
        5. alliesの ymlが存在すること
    """
    if "allies" not in stage_info.keys():
        raise KeyError("infoファイルの中に 'allies'が見つかりません")

    if "enemies" not in stage_info.keys():
        raise KeyError("infoファイルの中に 'enemies'が見つかりません")

    default_dir = "coding_yusha/assets"
    for enemy_yml in stage_info["enemies"]:
        if not path.exists(path.join(default_dir, stage, enemy_yml)):
            raise FileNotFoundError(f"敵の ymlファイルが見つかりません: {enemy_yml}")

    for ally_yml in stage_info["allies"]:
        if not path.exists(path.join(default_dir, stage, ally_yml)):
            raise FileNotFoundError(f"味方の ymlファイルが見つかりません: {ally_yml}")

    return True


def validate_ally_py_files(stage_info: dict[str, list[str]], ally_py_files: list[str]):
    """
        確認したいのは 2つ
        1. 味方の pyファイルの数が info.ymlの alliesの数と一致すること
        2. 味方の pyファイルの名前が info.ymlの alliesの名前と一致すること
    """
    if len(ally_py_files) != len(stage_info["allies"]):
        raise FileNotFoundError("味方の pyファイルの数が不正です")

    # 短く書くため、拡張子のリストを作って比較したい
    py_filenames = [path.splitext(path.basename(ally_py))[0] for ally_py in ally_py_files]
    yml_filenames = [path.splitext(path.basename(ally_yml))[0] for ally_yml in stage_info["allies"]]
    for py_filename in py_filenames:
        if py_filename not in yml_filenames:
            # TODO: 専用のエラークラスを作る
            raise FileNotFoundError(f"味方の pyファイルの名前が不正です: {py_filename}")
    return True


def map_files(stage: str, stage_info: dict[str, list[str]], ally_py_files: list[str]) \
        -> dict[str, str]:
    '''
    対応する pyファイルと ymlファイルを dictにまとめる
    '''
    default_dir = "coding_yusha/assets"
    map = {"allies": {}, "enemies": {}}
    for yml in stage_info["allies"]:
        name = path.splitext(yml)[0]
        py_filename = name + ".py"
        for ally_py in ally_py_files:
            if path.basename(ally_py) == py_filename:
                _map = {"yml": yml, "py": ally_py}
                map["allies"][name] = _map
    for yml in stage_info["enemies"]:
        name = path.splitext(yml)[0]
        py_path = path.join(default_dir, stage, name + ".py")
        _map = {"yml": yml, "py": py_path}
        map["enemies"][name] = _map
    return map


def generate_unit_from_py(unit_py: str) -> Unit:
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
        unit.attach_parameter("test", "ally_01.yml")
        return unit
    except Exception as e:
        original_error_str = f"{e.__class__.__name__}: {str(e)}"

    # TODO: 専用のエラークラスを作る
    # TODO: 呼び出し元で余計なスタックトレースを表示しないようにする
    raise Exception(
        f"Unitの生成に失敗しました: {unit_py}\n"
        + "指定された pyファイルで以下のエラーが発生しました\n"
        + original_error_str)


def initialize_units(stage: str, files_map: dict[str, dict[str, str]]) \
        -> tuple[list[Unit], list[Unit]]:
    allies = []
    enemies = []
    for key in files_map:
        for _, files in files_map[key].items():
            unit = generate_unit_from_py(files["py"])
            unit.attach_parameter(stage, files["yml"])
            if key == "allies":
                allies.append(unit)
            else:
                enemies.append(unit)
    return (allies, enemies)
