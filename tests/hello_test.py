from src.hello import hello
from src.hello import calc

def test_hello():
    assert hello() == "Hello, world!"

def test_calc():
    assert calc(1, 2) == 2