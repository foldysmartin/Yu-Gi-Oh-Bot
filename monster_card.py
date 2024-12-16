from dataclasses import dataclass
from uuid import UUID


@dataclass
class MonsterCard:
    instance_id: UUID
    name: str
    attack: int
    defence: int
    level: int
