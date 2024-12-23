from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Card:
    instance_id: UUID
    card_id: int
    name: str

