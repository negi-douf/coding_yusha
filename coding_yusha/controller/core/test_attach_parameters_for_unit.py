from coding_yusha.controller.core import attach_parameters_for_unit


def test_list_unit_files():
    dirname = "test"
    python_files = ["./ally_01.py", "public/test/ally_02.py"]
    expected_dict = {
        "allies": [
            {
                "py": python_files[0],
                "yml": "ally_01.yml",
            },
            {
                "py": python_files[1],
                "yml": "ally_02.yml",
            },
        ],
        "enemies": [
            {
                "py": "coding_yusha/assets/test/enemy_01.py",
                "yml": "enemy_01.yml",
            },
        ],
    }

    result_dict = attach_parameters_for_unit.list_unit_files(dirname, python_files)

    assert result_dict == expected_dict
