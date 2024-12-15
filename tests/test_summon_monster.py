from cards import find_card
from game import FieldHalf, Player, Zone


def test_can_summon_a_monster():
    monster = find_card("Mystical Elf")

    field_half = FieldHalf([monster])
    field_half = field_half.draw()

    
    field_half = field_half.activate(1, Zone.Third)

    assert field_half.monsterAt(Zone.Third) == monster
    assert field_half.numberOfCards() == 0
