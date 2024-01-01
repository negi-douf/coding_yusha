from coding_yusha.hello import hello
from coding_yusha.hello import calc


def test_hello():
    assert hello() == "Hello, world!"


def test_calc():
    assert calc(1, 2) == 2
