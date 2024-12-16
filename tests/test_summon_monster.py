from pytest import raises
from cards import find_card
from game import FieldHalf, SummoningError, Zone


def test_can_summon_a_monster():
    monster = find_card("Mystical Elf")

    field_half = FieldHalf([monster])
    field_half = field_half.draw()

    
    field_half = field_half.activate(1)

    assert field_half.monsterAt(Zone.First) == monster
    assert field_half.numberOfCards() == 0

def test_cannot_summon_if_zone_is_not_empty():
    monster = find_card("Mystical Elf")

    field_half = FieldHalf([monster, monster, monster, monster, monster, monster])
    

    # Fill all 5 zones
    for i in range(1, 6):
        field_half = field_half.draw()
        field_half = field_half.activate(1)


    with raises(SummoningError):
        field_half = field_half.draw()
        field_half.activate(1)
