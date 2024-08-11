from coding_yusha.controller.core.unit import Unit


class Enemy01(Unit):
    def run(self):
        self.nop()

    def nop(self):
        print(f'{self.name}はじっとしている')


def main():
    return Enemy01()
