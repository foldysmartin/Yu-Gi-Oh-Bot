from pytest import raises
from Field import Field
from invalid_target_error import InvalidTargetError
from field_half import FieldHalf
from abstract_field import Zone
from cards import find_card
from effects import Destroy
from monster_card import MonsterCard


def test_attacker_is_destroyed_if_other_card_has_greater_attack():
    attacker = find_card("Mystical Elf")
    defender = find_card("Giant Soldier of Stone")

    expected = Destroy(id=attacker.instance_id)
    outcome = attacker.battle(defender)

    assert expected in outcome


def test_defender_is_destroyed_if_attacker_has_greater_attack():
    attacker = find_card("Giant Soldier of Stone")
    defender = find_card("Mystical Elf")

    expected = Destroy(id=defender.instance_id)
    outcome = attacker.battle(defender)

    assert expected in outcome


def test_both_cards_are_destroyed_if_attack_is_equal():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    expected = [Destroy(id=attacker.instance_id), Destroy(id=defender.instance_id)]
    outcome = attacker.battle(defender)

    assert set(expected) <= set(outcome)


def test_battle_between_monsters():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster])
    field = Field(active_player=field_half, inactive_player=field_half)

    assert Destroy(id=monster.instance_id) in field.battle(Zone.First, Zone.First)


def test_battle_cannot_happen_if_no_monster_in_attack_zone():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster, None])
    field = Field(active_player=field_half, inactive_player=field_half)

    with raises(InvalidTargetError):
        field.battle(Zone.Second, Zone.First)


def test_battle_cannot_happen_if_no_monster_in_defense_zone():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster, None])
    field = Field(active_player=field_half, inactive_player=field_half)

    with raises(InvalidTargetError):
        field.battle(Zone.First, Zone.Second)
