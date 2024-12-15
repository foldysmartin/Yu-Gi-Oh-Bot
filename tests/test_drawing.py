from pytest import raises
from cards import find_card
from game import Game, Lost, Player


def test_draw_on_start():
    monster = find_card("Mystical Elf")
    player = Player(deck = [monster,monster,monster,monster,monster,monster])
    game = Game(player, player)

    assert game.player1.numberOfCards() == 6
    assert game.player2.numberOfCards() == 5

def test_cards_are_removed_from_deck():
    monster = find_card("Mystical Elf")
    player = Player(deck = [monster,monster,monster,monster,monster,monster])
    game = Game(player, player)

    assert game.player1.deck_size() == 0
    assert game.player2.deck_size() == 1

def test_end_turn_triggers_next_draw():
    monster = find_card("Mystical Elf")
    player = Player(deck = [monster,monster,monster,monster,monster,monster])
    game = Game(player, player)
    game.end_turn()
    
    assert game.player2.numberOfCards() == 6
    
def test_game_is_lost_if_cannot_draw():
    monster = find_card("Mystical Elf")
    player = Player(deck = [monster,monster,monster,monster,monster,monster])
    game = Game(player, player)
    with raises(Lost):
        game.end_turn()
        game.end_turn()

    