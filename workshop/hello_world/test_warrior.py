from workshop.hello_world import warrior


def test_main():
    unit = warrior.main()
    assert unit.__class__.__name__ == "Warrior"
