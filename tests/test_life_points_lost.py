from abstract_field import AbstractField
from cards import find_card
from effects import LoseLifePoints
from field_half import FieldHalf
from Player import Player
from game_state import GameState


def test_life_points_lost_attacker():
    attacker = find_card("Mystical Elf")
    defender = find_card("Giant Soldier of Stone")

    outcome = attacker.target_monster(defender)

    assert LoseLifePoints(attacker=True, life_points=500) in outcome


def test_life_points_lost_defender():
    attacker = find_card("Giant Soldier of Stone")
    defender = find_card("Mystical Elf")

    outcome = attacker.target_monster(defender)

    assert LoseLifePoints(attacker=False, life_points=500) in outcome


def test_attacking_directly_subtracts_life_points():
    attacker = find_card("Mystical Elf")

    outcome = attacker.target_directly()

    assert LoseLifePoints(attacker=False, life_points=800) in outcome


def test_life_points_are_subtracted_from_attacker():
    effect = LoseLifePoints(attacker=True, life_points=400)
    game_state = GameState()

    abstract_field = AbstractField(
        active_player=FieldHalf, inactive_player=FieldHalf([])
    )

    game_state, abstract_field = effect.apply(game_state, abstract_field)
    game_state.life_points(Player.One) == 7600


def test_life_points_are_subtracted_from_defender():
    effect = LoseLifePoints(attacker=False, life_points=400)
    game_state = GameState()

    abstract_field = AbstractField(
        active_player=FieldHalf, inactive_player=FieldHalf([])
    )

    game_state, abstract_field = effect.apply(game_state, abstract_field)
    game_state.life_points(Player.Two) == 7600
