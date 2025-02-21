from dataclasses import dataclass


@dataclass
class Update:
    time: float
    delta: float
    ticks: int
