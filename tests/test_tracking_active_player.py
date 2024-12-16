from cards import find_card
from game import Field, Player


def test_starting_active_player_is_player_1():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster]

    field = Field.game_start(deck, deck)
    assert field.current_player == Player.One

def test_switch_active_player():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster, monster]

    field = Field.game_start(deck, deck)
    field = field.end_turn()
    assert field.current_player == Player.Two

    field = field.end_turn()
    assert field.current_player == Player.One