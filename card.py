from dataclasses import dataclass
from uuid import UUID


@dataclass
class Card:
    instance_id: UUID

    def play_from_hand(self):
        raise NotImplementedError()
