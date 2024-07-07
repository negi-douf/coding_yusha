from coding_yusha.controller.core.unit import Unit


class Nop(Unit):
    def main(self):
        return self.nop()


def main():
    return Nop()
