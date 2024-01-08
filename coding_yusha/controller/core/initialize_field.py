from os import path

from yaml import safe_load


def initialize_field(stage: str, ally_py_files: list[str]):
    stage_info = load_stage_info(stage)
    validate_ally_py_files(stage_info, ally_py_files)


def load_stage_info(stage: str):
    default_yml_dir = "coding_yusha/assets"
    try:
        with open(path.join(default_yml_dir, stage, "info.yml"), "r", encoding="utf-8") as f:
            body = safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"infoファイルが見つかりません: {stage}") from e

    if "allies" not in body.keys():
        raise KeyError("infoファイルの中に 'allies'が見つかりません")

    if "enemies" not in body.keys():
        raise KeyError("infoファイルの中に 'enemies'が見つかりません")

    return body


def validate_ally_py_files(stage_info: dict[str, list[str]], ally_py_files: list[str]):
    """
        確認したいのは 2つ
        1. 味方の pyファイルの数が info.ymlの alliesの数と一致すること
        2. 味方の pyファイルの名前が info.ymlの alliesの名前と一致すること
    """
    if len(ally_py_files) != len(stage_info["allies"]):
        raise FileNotFoundError("味方の pyファイルの数が不正です")

    # 短く書くため、拡張子だけのリストを作って比較したい
    py_filenames = [path.splitext(path.basename(ally_py))[0] for ally_py in ally_py_files]
    yml_filenames = [path.splitext(path.basename(ally_yml))[0] for ally_yml in stage_info["allies"]]
    for py_filename in py_filenames:
        if py_filename not in yml_filenames:
            # TODO: 専用のエラークラスを作る
            raise FileNotFoundError(f"味方の pyファイルの名前が不正です: {py_filename}")
    return True
