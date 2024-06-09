from coding_yusha.controller.core.unit import Unit


class Enemy01(Unit):
    def main(self):
        self.nop()

    def nop(self):
        print(f'{self.name}はじっとしている')


def main():
    return Enemy01()
