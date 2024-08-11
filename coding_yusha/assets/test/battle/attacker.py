from coding_yusha.controller.core.unit import Unit


class Attacker(Unit):
    def run(self):
        event = self.attack("nop")
        return event


def main():
    return Attacker()
