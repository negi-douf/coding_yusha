from coding_yusha.controller.core.unit import Unit


class Enemy01(Unit):
    def run(self):
        pass
        # passにすると親クラスの runメソッドが呼ばれる


def main():
    return Enemy01()
