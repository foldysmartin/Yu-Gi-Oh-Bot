from functools import reduce

from pytest import raises
from Player import Player
from abstract_field import AbstractField, AbstractFieldHalf, NoMonsterError, Zone
from battling.to_battle import AttackTarget, InvalidTargetError, ToBattle
from cards.load_card import find_card
from game_state import GameState


def test_attacker_is_destroyed_if_other_card_has_greater_attack():
    attacker = find_card("Mystical Elf")
    defender = find_card("Giant Soldier of Stone")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters=[attacker]),
        AbstractFieldHalf(deck=[], monsters=[defender]),
    )
    game_state = GameState()

    effects = ToBattle(Zone.First, AttackTarget.First).activate(
        abstract_field, game_state
    )

    for effect in effects:
        abstract_field, game_state = effect.apply(abstract_field, game_state)

    assert abstract_field.active_player.monster_count() == 0
    assert abstract_field.inactive_player.monster_count() == 1
    assert game_state.life_points(Player.One) == 7500


def test_defender_is_destroyed_if_attacker_has_greater_attack():
    attacker = find_card("Giant Soldier of Stone")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters=[attacker]),
        AbstractFieldHalf(deck=[], monsters=[defender]),
    )
    game_state = GameState()

    effects = ToBattle(Zone.First, AttackTarget.First).activate(
        abstract_field, game_state
    )

    for effect in effects:
        abstract_field, game_state = effect.apply(abstract_field, game_state)

    assert abstract_field.active_player.monster_count() == 1
    assert abstract_field.inactive_player.monster_count() == 0
    assert game_state.life_points(Player.Two) == 7500


def test_both_cards_are_destroyed_if_attack_is_equal():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters=[attacker]),
        AbstractFieldHalf(deck=[], monsters=[defender]),
    )
    game_state = GameState()

    effects = ToBattle(Zone.First, AttackTarget.First).activate(
        abstract_field, game_state
    )

    for effect in effects:
        abstract_field, game_state = effect.apply(abstract_field, game_state)

    assert abstract_field.active_player.monster_count() == 0
    assert abstract_field.inactive_player.monster_count() == 0


def test_battle_cannot_happen_if_no_monster_in_attack_zone():
    monster = find_card("Mystical Elf")
    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters=[monster]),
        AbstractFieldHalf(deck=[], monsters=[monster]),
    )
    game_state = GameState()

    with raises(NoMonsterError):
        ToBattle(Zone.Second, AttackTarget.First).activate(abstract_field, game_state)


def test_battle_cannot_happen_if_no_monster_in_defense_zone():
    monster = find_card("Mystical Elf")
    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters=[monster]),
        AbstractFieldHalf(deck=[], monsters=[monster]),
    )
    game_state = GameState()

    with raises(NoMonsterError):
        ToBattle(Zone.First, AttackTarget.Second).activate(abstract_field, game_state)


def test_attack_directly():
    monster = find_card("Mystical Elf")
    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters=[monster]),
        AbstractFieldHalf(deck=[], monsters=[]),
    )
    game_state = GameState()

    effects = ToBattle(Zone.First, AttackTarget.Direct).activate(
        abstract_field, game_state
    )

    for effect in effects:
        abstract_field, game_state = effect.apply(abstract_field, game_state)

    assert abstract_field.active_player.monster_count() == 1
    assert abstract_field.inactive_player.monster_count() == 0
    assert game_state.life_points(Player.Two) == 7200


def test_cannot_attack_directly_if_there_is_a_monster():
    monster = find_card("Mystical Elf")
    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters=[monster]),
        AbstractFieldHalf(deck=[], monsters=[monster]),
    )
    game_state = GameState()

    with raises(InvalidTargetError):
        ToBattle(Zone.First, AttackTarget.Direct).activate(abstract_field, game_state)
