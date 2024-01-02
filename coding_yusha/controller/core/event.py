from abc import ABC


class Event(ABC):
    sender: str
    target: str
    move: str
