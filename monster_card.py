from dataclasses import dataclass

@dataclass
class MonsterCard:
    name: str
    attack: int
    defence: int
    level: int