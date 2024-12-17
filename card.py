from dataclasses import dataclass
from uuid import UUID


@dataclass
class Card:
    instance_id: UUID

    def activate(self):
        raise NotImplementedError()
