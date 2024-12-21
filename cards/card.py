from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Card:
    instance_id: UUID
    name: str

    activator: callable

    def activate(self):
        return self.activator(self)
