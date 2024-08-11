from coding_yusha.controller.core.unit import Unit


class Nop(Unit):
    def run(self):
        return self.nop()


def main():
    return Nop()
