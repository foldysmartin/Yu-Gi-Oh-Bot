from cards import find_card
from game import Field, Player, Game


def test_starting_active_player_is_player_1():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster]

    game = Game.start(deck, deck)
    assert game.current_player == Player.One


def test_switch_active_player():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster, monster]

    game = Game.start(deck, deck)
    game.end_turn()
    assert game.current_player == Player.Two

    game.end_turn()
    assert game.current_player == Player.One


def test_get_hand():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster, monster]

    game = Game.start(deck, deck)
    assert len(game.fetch_hand(Player.One)) == 6
    assert len(game.fetch_hand(Player.Two)) == 5


def test_get_monsters():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster, monster]

    game = Game.start(deck, deck)

    game.activate(1)
    assert len(game.fetch_monsters(Player.One)) == 5
    game.fetch_monsters(Player.One)[0] == monster
