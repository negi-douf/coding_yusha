from dataclasses import dataclass


@dataclass(frozen=True)
class UnitRecord():
    name: str
    max_hp: int
    current_hp: int
    max_mp: int
    current_mp: int
