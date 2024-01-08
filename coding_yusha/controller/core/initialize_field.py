from os import path

from yaml import safe_load


def initialize_field(stage: str, *ally_py_files: str):
    _ = load_stage_info(stage)


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
