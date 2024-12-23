from dataclasses import dataclass

from Player import Player
from Field import Field
from game_state import GameState, Phase
from battling.to_battle import AttackTarget
from summoning.normal.to_normal_summon import ToNormalSummon

@dataclass(frozen=True)
class ToNextPhase:
    def activate(self, field, game_state):
        return NextPhase()

@dataclass(frozen=True)
class NextPhase:
    def apply(self, field, game_state):
        game_state = game_state.change_phase()
        if game_state.phase == Phase.Draw:
            field = field.end_turn()
            game_state = game_state.change_phase()
        return field, game_state


@dataclass()
class Game:
    field: Field
    game_state: GameState = GameState()

    def start(deck_1, deck_2):
        field = Field.game_start(deck_1, deck_2)
        return Game(field)

    def next_phase(self):
        self.game_state = self.game_state.change_phase()
        if self.game_state.phase == Phase.Draw:
            self.field = self.field.end_turn()
            self.game_state = self.game_state.change_phase()

    def can_battle(self):
        for zone in self.fetch_monsters(self.game_state.active_player):
            for target in AttackTarget:
                try:
                    self.field.attack(zone, target).activate(
                        self.field, self.game_state
                    )
                    return True
                except:
                    pass
        return False

    def fetch_hand(self, player):
        return self._fetch_field(player).hand

    def fetch_monsters(self, player):
        return self._fetch_field(player).monsters

    def avaliable_actions(self):
        return list(self._avaliable_actions())
    
    def still_playing(self):
        return (not self.game_state.life_points(Player.One) <= 0
            and not self.game_state.life_points(Player.Two) <= 0)

    
    def _avaliable_actions(self):
        for i in range(len(self.fetch_hand(self.game_state.active_player))):
            try:
                action = ToNormalSummon(i)
                action.activate(self.field, self.game_state)
                yield action
            except:
                pass

        for zone in self.fetch_monsters(self.game_state.active_player):
            for target in AttackTarget:
                try:
                    action = self.field.attack(zone, target)
                    action.activate(self.field, self.game_state)
                    yield action
                except:
                    pass
        yield ToNextPhase()

    def trigger_action(self, action):
        effects = action.activate(self.field, self.game_state)
        self.field, self.game_state = effects.apply(self.field, self.game_state)

    def _fetch_field(self, player):
        return (
            self.field.active_player
            if player == self.game_state.active_player
            else self.field.inactive_player
        )
