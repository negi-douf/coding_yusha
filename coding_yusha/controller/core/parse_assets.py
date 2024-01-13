from os import path

from yaml import safe_load


def load_stage_info(stage: str) -> dict[str, list[str]]:
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
        1. stageの keyが存在すること
        2. dirの keyが存在すること
        3. alliesの keyが存在すること
        4. enemiesの keyが存在すること
        5. enemiesの ymlが存在すること
        6. enemiesの pyが存在すること
        7. alliesの ymlが存在すること
    """
    if "stage" not in stage_info.keys():
        raise KeyError("infoファイルの中に 'stage'が見つかりません")
    if "dir" not in stage_info.keys():
        raise KeyError("infoファイルの中に 'dir'が見つかりません")
    if "allies" not in stage_info.keys():
        raise KeyError("infoファイルの中に 'allies'が見つかりません")
    if "enemies" not in stage_info.keys():
        raise KeyError("infoファイルの中に 'enemies'が見つかりません")

    for enemy_yml in stage_info["enemies"]:
        if not path.exists(path.join(stage_info["dir"], enemy_yml)):
            raise FileNotFoundError(f"敵の ymlファイルが見つかりません: {enemy_yml}")

    for ally_yml in stage_info["allies"]:
        if not path.exists(path.join(stage_info["dir"], ally_yml)):
            raise FileNotFoundError(f"味方の ymlファイルが見つかりません: {ally_yml}")

    return True


def map_ally_files(stage_info: dict[str, list[str]], ally_py_files: list[str]) -> dict[str, str]:
    validate_ally_py_files(stage_info, ally_py_files)
    ally_names = [path.splitext(yml)[0] for yml in stage_info["allies"]]
    map = {}
    for ally_name in ally_names:
        for ally_py in ally_py_files:
            if path.splitext(path.basename(ally_py))[0] == ally_name:
                file_pair = {
                    "py": ally_py,
                    "yml": path.join(stage_info["dir"], ally_name + ".yml"),
                }
                map[ally_name] = file_pair
    return map


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


def map_enemy_files(stage_info: dict[str, list[str]]) -> dict[str, str]:
    # validationは済んでいるはず
    map = {}
    for yml in stage_info["enemies"]:
        file_pair = {
            "py": path.join(stage_info["dir"], yml.replace(".yml", ".py")),
            "yml": path.join(stage_info["dir"], yml),
        }
        enemy_name = path.splitext(path.basename(yml))[0]
        map[enemy_name] = file_pair
    return map
