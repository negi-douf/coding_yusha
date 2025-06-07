from dataclasses import dataclass

from coding_yusha.controller.core.event import Event


@dataclass(frozen=True)
class EventRecord():
    turn_num: int
    event: Event
