from Field import Field
from Player import Player
from cards import find_card
from game import Game
from game_state import GameState


def test_starting_active_player_is_player_1():
    gamestate = GameState()
    assert gamestate.active_player == Player.One


def test_switch_active_player():
    gamestate = GameState()
    gamestate = gamestate.end_turn()
    assert gamestate.active_player == Player.Two

    gamestate = gamestate.end_turn()
    assert gamestate.active_player == Player.One


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

    game.play_from_hand(1)
    assert len(game.fetch_monsters(Player.One)) == 5
    game.fetch_monsters(Player.One)[0] == monster
