from yaml import safe_load

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
    is_guarding: bool  # ガード中かどうか

    def attach_parameter(self, yml_file: str):
        # NOTE: ymlからしかパラメータを設定できないのは不便かもしれない
        try:
            with open(yml_file, "r", encoding="utf-8") as f:
                body = safe_load(f)
            self.name = body["unit"]["name"]
            self.max_hp = body["unit"]["max_hp"]
            self.current_hp = body["unit"]["current_hp"]
            self.max_mp = body["unit"]["max_mp"]
            self.current_mp = body["unit"]["current_mp"]
            self.pa = body["unit"]["pa"]
            self.pd = body["unit"]["pd"]
            self.ma = body["unit"]["ma"]
            self.md = body["unit"]["md"]
            self.agi = body["unit"]["agi"]
            self.is_guarding = False
        except FileNotFoundError as e:
            raise FileNotFoundError(f"ymlファイルが見つかりません: {yml_file}") from e
        except KeyError as e:
            raise KeyError(f"Unitの初期化に必要なパラメータが見つかりません: {yml_file}") from e

    def is_dead(self) -> bool:
        return self.current_hp <= 0

    def reset_status(self):
        self.is_guarding = False

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

    def run(self):
        pass

    def _equals(self, other: "Unit") -> bool:
        return (
            self.name == other.name and
            self.max_hp == other.max_hp and
            self.current_hp == other.current_hp and
            self.max_mp == other.max_mp and
            self.current_mp == other.current_mp and
            self.pa == other.pa and
            self.pd == other.pd and
            self.ma == other.ma and
            self.md == other.md and
            self.agi == other.agi
        )
