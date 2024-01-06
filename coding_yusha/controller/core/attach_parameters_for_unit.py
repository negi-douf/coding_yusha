from os import path

from yaml import safe_load

# from coding_yusha.controller.core import attach_parameters_for_unit
# from coding_yusha.controller.core.unit import Unit


def load_info(dirname: str):
    default_yml_dir = "coding_yusha/assets"
    try:
        with open(path.join(default_yml_dir, dirname, "info.yml"), "r", encoding="utf-8") as f:
            body = safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError("ファイルが見つかりません。") from e

    if "allies" not in body.keys():
        raise KeyError("alliesが見つかりません。")

    if "enemies" not in body.keys():
        raise KeyError("enemiesが見つかりません。")

    return body


def list_unit_files(dirname: str, python_files: list[str]) -> dict[str, list[dict[str, str]]]:
    (allies, enemies) = load_info(dirname).values()

    # TODO: alliesのバリデーションをきりだす
    ally_files = []
    for ally in allies:
        for python_file in python_files:
            filename_from_info = path.splitext(ally)[0]
            filename_from_python = path.splitext(path.basename(python_file))[0]
            if filename_from_info == filename_from_python:
                ally_files.append({
                    "py": python_file,
                    "yml": f"coding_yusha/assets/{dirname}/{ally}",
                })

    enemy_files = []
    for enemy in enemies:
        filename_from_info = path.splitext(enemy)[0]
        enemy_files.append({
            "py": f"coding_yusha/assets/{dirname}/{filename_from_info}.py",
            "yml": f"coding_yusha/assets/{dirname}/{enemy}",
        })

    return {
        "allies": ally_files,
        "enemies": enemy_files,
    }
