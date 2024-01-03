from coding_yusha.controller.core import attach_parameters_for_unit
from coding_yusha.controller.core.unit import Unit


def test_list_unit_files():
    dirname = "test"
    python_files = ["./ally_01.py", "public/test/ally_02.py"]
    expected_dict = {
        "allies": [
            {
                "py": python_files[0],
                "yml": "coding_yusha/assets/test/ally_01.yml",
            },
            {
                "py": python_files[1],
                "yml": "coding_yusha/assets/test/ally_02.yml",
            },
        ],
        "enemies": [
            {
                "py": "coding_yusha/assets/test/enemy_01.py",
                "yml": "coding_yusha/assets/test/enemy_01.yml",
            },
        ],
    }

    result_dict = attach_parameters_for_unit.list_unit_files(dirname, python_files)

    assert result_dict == expected_dict


def test_create_unit_list_from_files():
    files = {
        "allies": [
            {
                "py": "coding_yusha/assets/test/ally_01.py",
                "yml": "coding_yusha/assets/test/ally_01.yml",
            },
        ],
        "enemies": [
            {
                "py": "coding_yusha/assets/test/enemy_01.py",
                "yml": "coding_yusha/assets/test/enemy_01.yml",
            },
        ],
    }
    expected_ally_01 = Unit("ally_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    expected_enemy_01 = Unit("enemy_01", 10, 10, 10, 10, 10, 10, 10, 10, 10)
    expected_unit_list = {
        "allies": [expected_ally_01],
        "enemies": [expected_enemy_01],
    }

    result_unit_list = attach_parameters_for_unit.create_unit_list_from_files(files)

    assert result_unit_list["allies"][0]._equals(expected_unit_list["allies"][0])
    assert result_unit_list["enemies"][0]._equals(expected_unit_list["enemies"][0])
