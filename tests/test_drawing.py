from pytest import raises
from cards import find_card
from game import Field, OutOfCards


def test_draw_on_start():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster]
    field = Field.game_start(deck, deck)

    assert field.active_player.numberOfCards() == 6
    assert field.inactive_player.numberOfCards() == 5


def test_cards_are_removed_from_deck():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster]
    field = Field.game_start(deck, deck)

    assert field.active_player.deck_size() == 0
    assert field.inactive_player.deck_size() == 1


def test_end_turn_triggers_next_draw():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster]
    field = Field.game_start(deck, deck)
    field = field.end_turn()

    assert field.active_player.numberOfCards() == 6


def test_game_is_lost_if_cannot_draw():
    monster = find_card("Mystical Elf")
    deck = [monster, monster, monster, monster, monster, monster]
    field = Field.game_start(deck, deck)
    with raises(OutOfCards):
        field = field.end_turn()
        field = field.end_turn()
