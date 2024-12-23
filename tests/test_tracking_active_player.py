from abstract_field import Zone
from cards.load_card import find_card
from Player import Player
from game import Game
from game_state import GameState
from summoning.normal.to_normal_summon import ToNormalSummon


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
    
    game.trigger_action(ToNormalSummon(index=0))
    assert len(game.fetch_monsters(Player.One)) == 1
    game.fetch_monsters(Player.One)[Zone.First] == monster
