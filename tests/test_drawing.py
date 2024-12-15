from game import Game, Player


def test_draw_on_start():
    player = Player(deck = [1,1,1,1,1,1])
    game = Game(player, player)

    assert game.player1.numberOfCards() == 6
    assert game.player2.numberOfCards() == 5

def test_cards_are_removed_from_deck():
    player = Player(deck = [1,1,1,1,1,1])
    game = Game(player, player)

    assert game.player1.deck_size() == 0
    assert game.player2.deck_size() == 1
    