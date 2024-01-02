from abc import ABC, abstractmethod


class Unit(ABC):
    max_hp: int  # 最大HP
    current_hp: int  # 現在HP
    max_mp: int  # 最大MP
    current_mp: int  # 現在MP
    pa: int  # 物理攻撃力
    pd: int  # 物理防御力
    ma: int  # 魔法攻撃力
    md: int  # 魔法防御力
    agi: int  # 素早さ

    @abstractmethod
    def attack(self, target):
        """

        選択したUnitに通常攻撃を行う

        Args:
            target: 攻撃対象
        """
        pass

    @abstractmethod
    def special_move(self, target=None):
        """

        選択したUnitに特技を使う

        Args:
            target: 対象
        """
        pass

    @abstractmethod
    def guard(self):
        """
        Unitからの攻撃をガードする
        """
        pass
