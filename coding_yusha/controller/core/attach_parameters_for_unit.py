from os import path

from yaml import safe_load


def load_info(dirname: str):
    default_yml_dir = "coding_yusha/assets"
    try:
        with open(path.join(default_yml_dir, dirname, "info.yml"), "r", encoding="utf-8") as f:
            body = safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError("infoファイルが見つかりません。") from e

    if "allies" not in body.keys():
        raise KeyError("infoファイルの中に 'allies'が見つかりません。")

    if "enemies" not in body.keys():
        raise KeyError("infoファイルの中に 'enemies'が見つかりません。")

    return body


def list_unit_files(dirname: str, python_files: list[str]) -> dict[str, list[dict[str, str]]]:
    (allies, enemies) = load_info(dirname).values()

    # TODO: alliesの pyファイルの存在を確認するバリデーション
    ally_files = []
    for ally_yml in allies:
        for python_file in python_files:
            filename_from_info = path.splitext(ally_yml)[0]
            filename_from_python = path.splitext(path.basename(python_file))[0]
            if filename_from_info == filename_from_python:
                ally_files.append({
                    "py": python_file,
                    "yml": f"coding_yusha/assets/{dirname}/{ally_yml}",
                })

    enemy_files = []
    for enemy_yml in enemies:
        filename_from_info = path.splitext(enemy_yml)[0]
        enemy_files.append({
            "py": f"coding_yusha/assets/{dirname}/{filename_from_info}.py",
            "yml": f"coding_yusha/assets/{dirname}/{enemy_yml}",
        })

    return {
        "allies": ally_files,
        "enemies": enemy_files,
    }


# def create_unit_list_from_files(files: dict[str, list[dict[str, str]]]) -> dict[str, list[Unit]]:
#     unit_list = {}
#     for allies_or_enemies, file_pair_list in files.items():
#         unit_list[allies_or_enemies] = []
#         for py_and_yml in file_pair_list:
#             unit = Unit.create_unit_from_file(py_and_yml["py"], py_and_yml["yml"])
#             unit_list[allies_or_enemies].append(unit)
#     return unit_list
