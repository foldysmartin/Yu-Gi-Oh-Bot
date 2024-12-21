from functools import reduce

from pytest import raises
from Player import Player
from abstract_field import AbstractField, AbstractFieldHalf, NoMonsterError, Zone
from battling.to_battle import AttackTarget, BattleError, ToBattle
from cards.load_card import find_card
from game_state import GameState, Phase


def test_attacker_is_destroyed_if_other_card_has_greater_attack():
    attacker = find_card("Mystical Elf")
    defender = find_card("Giant Soldier of Stone")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    abstract_field, game_state = (
        ToBattle(Zone.First, AttackTarget.First)
        .activate(abstract_field, game_state)
        .apply(abstract_field, game_state)
    )

    assert abstract_field.active_player.monster_count() == 0
    assert abstract_field.inactive_player.monster_count() == 1
    assert game_state.life_points(Player.One) == 7500


def test_defender_is_destroyed_if_attacker_has_greater_attack():
    attacker = find_card("Giant Soldier of Stone")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    abstract_field, game_state = (
        ToBattle(Zone.First, AttackTarget.First)
        .activate(abstract_field, game_state)
        .apply(abstract_field, game_state)
    )

    assert abstract_field.active_player.monster_count() == 1
    assert abstract_field.inactive_player.monster_count() == 0
    assert game_state.life_points(Player.Two) == 7500


def test_both_cards_are_destroyed_if_attack_is_equal():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    abstract_field, game_state = (
        ToBattle(Zone.First, AttackTarget.First)
        .activate(abstract_field, game_state)
        .apply(abstract_field, game_state)
    )

    assert abstract_field.active_player.monster_count() == 0
    assert abstract_field.inactive_player.monster_count() == 0


def test_battle_cannot_happen_if_no_monster_in_attack_zone():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    with raises(NoMonsterError):
        ToBattle(Zone.Second, AttackTarget.First).activate(abstract_field, game_state)


def test_battle_cannot_happen_if_no_monster_in_defense_zone():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    with raises(NoMonsterError):
        ToBattle(Zone.First, AttackTarget.Second).activate(abstract_field, game_state)


def test_attack_directly():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    abstract_field, game_state = (
        ToBattle(Zone.First, AttackTarget.Direct)
        .activate(abstract_field, game_state)
        .apply(abstract_field, game_state)
    )

    assert abstract_field.active_player.monster_count() == 1
    assert abstract_field.inactive_player.monster_count() == 0
    assert game_state.life_points(Player.Two) == 7200


def test_cannot_attack_directly_if_there_is_a_monster():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    with raises(BattleError):
        ToBattle(Zone.First, AttackTarget.Direct).activate(abstract_field, game_state)


def test_can_only_attack_in_battle_phase():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(turn=2)

    with raises(Exception):
        ToBattle(Zone.First, AttackTarget.First).activate(abstract_field, game_state)


def test_cannot_attack_on_turn_one():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={Zone.First: defender}),
    )
    game_state = GameState(phase=Phase.Battle, turn=1)

    with raises(Exception):
        ToBattle(Zone.First, AttackTarget.First).activate(abstract_field, game_state)


def test_monster_can_only_attack_once_per_turn():
    attacker = find_card("Mystical Elf")
    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    abstract_field, game_state = (
        ToBattle(Zone.First, AttackTarget.Direct)
        .activate(abstract_field, game_state)
        .apply(abstract_field, game_state)
    )

    with raises(Exception):
        ToBattle(Zone.First, AttackTarget.Direct).activate(abstract_field, game_state)


def test_can_attack_again_next_turn():
    attacker = find_card("Mystical Elf")
    abstract_field = AbstractField(
        AbstractFieldHalf(deck=[], monsters={Zone.First: attacker}),
        AbstractFieldHalf(deck=[], monsters={}),
    )
    game_state = GameState(phase=Phase.Battle, turn=2)

    abstract_field, game_state = (
        ToBattle(Zone.First, AttackTarget.Direct)
        .activate(abstract_field, game_state)
        .apply(abstract_field, game_state)
    )

    game_state = game_state.end_turn()
    game_state = game_state.end_turn()
    game_state = game_state.change_phase()
    game_state = game_state.change_phase()

    abstract_field, game_state = (
        ToBattle(Zone.First, AttackTarget.Direct)
        .activate(abstract_field, game_state)
        .apply(abstract_field, game_state)
    )

    assert game_state.life_points(Player.Two) == 6400
