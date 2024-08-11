from coding_yusha.controller.core import generate_unit


def test_generate_unit_from_py_parameters():
    ally_01 = generate_unit.generate_unit_from_py(
        "coding_yusha/assets/test/ally_01.py",
        "coding_yusha/assets/test/ally_01.yml")

    assert ally_01.name == "ally_01"
    assert ally_01.max_hp == 10
    assert ally_01.current_hp == 10
    assert ally_01.max_mp == 10
    assert ally_01.current_mp == 10
    assert ally_01.pa == 10
    assert ally_01.pd == 10
    assert ally_01.ma == 10
    assert ally_01.md == 10


def test_generate_unit_from_py_main(capsys):
    ally_01 = generate_unit.generate_unit_from_py(
        "coding_yusha/assets/test/ally_01.py",
        "coding_yusha/assets/test/ally_01.yml")

    ally_01.run()

    captured = capsys.readouterr()
    assert captured.out == "Ally01\n"
    assert captured.err == ""
