from pytest import raises
from FieldHalf import FieldHalf, HandEmptyError, Zone
from cards import find_card
from effects import Summon, SummoningError


def test_normal_cards_trigger_summoning():
    monster = find_card("Mystical Elf")
    assert type(monster.activate()) == Summon


def test_can_summon_a_monster():
    monster = find_card("Mystical Elf")

    field_half = FieldHalf([monster])
    field_half = field_half.draw()
    field_half = monster.activate().apply(field_half)

    assert field_half.monsterAt(Zone.First) == monster
    assert field_half.numberOfCards() == 0


def test_cannot_summon_if_zone_is_not_empty():
    monster = find_card("Mystical Elf")

    field_half = FieldHalf([monster, monster, monster, monster, monster, monster])

    # Fill all 5 zones
    for i in range(1, 6):
        field_half = field_half.draw()
        field_half = monster.activate().apply(field_half)

    with raises(SummoningError):
        field_half = field_half.draw()
        monster.activate().apply(field_half)
