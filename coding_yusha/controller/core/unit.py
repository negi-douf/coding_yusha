from coding_yusha.controller.core.event import Event


class Unit():
    name: str  # 名前。戦闘の中でユニークである必要がある
    max_hp: int  # 最大HP
    current_hp: int  # 現在HP
    max_mp: int  # 最大MP
    current_mp: int  # 現在MP
    pa: int  # 物理攻撃力
    pd: int  # 物理防御力
    ma: int  # 魔法攻撃力
    md: int  # 魔法防御力
    agi: int  # 素早さ

    def __init__(self, name: str, max_hp: int, current_hp: int, max_mp: int, current_mp: int,
                 pa: int, pd: int, ma: int, md: int, agi: int):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.max_mp = max_mp
        self.current_mp = current_mp
        self.pa = pa
        self.pd = pd
        self.ma = ma
        self.md = md
        self.agi = agi

    def attack(self, target: str):
        """

        選択したUnitに通常攻撃を行う

        Args:
            target (str): 攻撃対象
        """
        return Event(self.name, target, "attack")

    def special_move(self, target: str = None):
        """

        選択したUnitに特技を使う

        Args:
            target (str): 対象
        """
        return Event(self.name, target, "special_move")

    def guard(self):
        """
        Unitからの攻撃をガードする
        """
        return Event(self.name, self.name, "guard")
