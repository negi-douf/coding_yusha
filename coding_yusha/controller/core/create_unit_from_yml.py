from os import path

from yaml import safe_load

from coding_yusha.controller.core.unit import Unit


def create_unit_from_yml(directory, filename):
    default_yml_dir = "coding_yusha/assets"
    try:
        with open(path.join(default_yml_dir, directory, filename), "r", encoding="utf-8") as f:
            body = safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError("ファイルが見つかりません。") from e
    try:
        unit = Unit(
            name=body["unit"]["name"],
            max_hp=body["unit"]["max_hp"],
            current_hp=body["unit"]["current_hp"],
            max_mp=body["unit"]["max_mp"],
            current_mp=body["unit"]["current_mp"],
            pa=body["unit"]["pa"],
            pd=body["unit"]["pd"],
            ma=body["unit"]["ma"],
            md=body["unit"]["md"],
            agi=body["unit"]["agi"],
        )
    except KeyError as e:
        raise KeyError('Unitの初期化に必要なパラメータが見つかりません。') from e
    return unit
