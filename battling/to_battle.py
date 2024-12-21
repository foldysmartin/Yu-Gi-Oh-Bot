from dataclasses import dataclass
from enum import Enum
from abstract.action import Action
from abstract.effect import Effects
from abstract_field import AbstractField, Zone
from battling.attack import Attack
from battling.destroy import Destroy
from battling.lose_life_points import LoseLifePoints
from game_state import GameState, Phase


class AttackTarget(Enum):
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Fith = 4
    Direct = 5


class BattleError(Exception):
    pass


@dataclass(frozen=True)
class ToBattle(Action):
    zone: Zone
    target: AttackTarget

    def activate(self, field: AbstractField, game_state: GameState):
        if game_state.phase is not Phase.Battle:
            raise Exception("Can only attack in battle phase")

        if game_state.turn <= 1:
            raise Exception("Cannot attack on first turn")

        attacker = field.active_player.monsterAt(self.zone)
        if attacker in game_state.previous_attacks:
            raise Exception("Cannot attack with the same monster twice in one turn")

        attack = Attack(attacker)
        if self.target == AttackTarget.Direct:
            return attack + self._attack_directly(attacker, game_state, field)
        else:
            return attack + self._attack_monster(attacker, field, game_state)

    def _attack_directly(self, attacker, game_state, field):
        if field.inactive_player.monster_count() > 0:
            raise BattleError("Cannot attack directly if there is a monster")

        return LoseLifePoints(attacker.attack, game_state.inactive_player)

    def _attack_monster(self, attacker, field, game_state):
        zone = Zone(self.target.value)
        defender = field.inactive_player.monsterAt(zone)

        if attacker.attack > defender.attack:
            return Destroy(defender) + LoseLifePoints(
                attacker.attack - defender.attack, game_state.inactive_player
            )

        elif attacker.attack < defender.attack:
            return Destroy(attacker) + LoseLifePoints(
                defender.attack - attacker.attack, game_state.active_player
            )

        else:
            return Destroy(attacker) + Destroy(defender)
