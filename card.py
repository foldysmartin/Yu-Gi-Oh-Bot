from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Card:
    instance_id: UUID

    def play_from_hand(self):
        raise NotImplementedError()
