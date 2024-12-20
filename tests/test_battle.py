from pytest import raises
from Field import BattleTarget, Field
from invalid_target_error import InvalidTargetError
from field_half import FieldHalf
from abstract_field import Zone
from cards import find_card
from effects import Destroy, LoseLifePoints
from monster_card import MonsterCard


def test_attacker_is_destroyed_if_other_card_has_greater_attack():
    attacker = find_card("Mystical Elf")
    defender = find_card("Giant Soldier of Stone")

    outcome = attacker.target_monster(defender)

    assert Destroy(id=defender.instance_id) not in outcome
    assert Destroy(id=attacker.instance_id) in outcome


def test_defender_is_destroyed_if_attacker_has_greater_attack():
    attacker = find_card("Giant Soldier of Stone")
    defender = find_card("Mystical Elf")

    outcome = attacker.target_monster(defender)

    assert Destroy(id=defender.instance_id) in outcome
    assert Destroy(id=attacker.instance_id) not in outcome


def test_both_cards_are_destroyed_if_attack_is_equal():
    attacker = find_card("Mystical Elf")
    defender = find_card("Mystical Elf")

    outcome = attacker.target_monster(defender)

    assert Destroy(id=defender.instance_id) in outcome
    assert Destroy(id=attacker.instance_id) in outcome


def test_battle_between_monsters():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster])
    field = Field(active_player=field_half, inactive_player=field_half)

    assert Destroy(id=monster.instance_id) in field.attack(Zone.First, Zone.First)


def test_battle_cannot_happen_if_no_monster_in_attack_zone():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster, None])
    field = Field(active_player=field_half, inactive_player=field_half)

    with raises(InvalidTargetError):
        field.attack(Zone.Second, Zone.First)


def test_battle_cannot_happen_if_no_monster_in_defense_zone():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster, None])
    field = Field(active_player=field_half, inactive_player=field_half)

    with raises(InvalidTargetError):
        field.attack(Zone.First, Zone.Second)


def test_can_attack_directly():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster])
    field = Field(
        active_player=field_half,
        inactive_player=FieldHalf(
            deck=[],
        ),
    )

    assert LoseLifePoints(attacker=False, life_points=800) in field.attack(
        Zone.First, BattleTarget.Direct
    )


def test_cannot_attack_directly_if_there_are_monsters_on_the_field():
    monster = find_card("Mystical Elf")
    field_half = FieldHalf(deck=[], hand=[], monsters=[monster])
    field = Field(
        active_player=field_half,
        inactive_player=field_half,
    )

    with raises(InvalidTargetError):
        field.attack(Zone.First, BattleTarget.Direct)
