from cards import find_card
from game import Player, Zone


def test_can_summon_a_monster():
    monster = find_card("Mystical Elf")

    player = Player([monster])
    player = player.draw()

    
    player = player.activate(1, Zone.Third)

    assert player.monsterAt(Zone.Third) == monster
    assert player.numberOfCards() == 0
