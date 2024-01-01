from coding_yusha.hello import calc, hello


def test_hello():
    assert hello() == "Hello, world!"


def test_calc():
    assert calc(1, 2) == 2
