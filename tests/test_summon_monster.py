from pytest import raises
from field_half import FieldHalf, HandEmptyError, Zone
from abstract_field import AbstractField
from cards import find_card
from effects import Summon, SummoningError
from game_state import GameState


def test_normal_cards_trigger_summoning():
    monster = find_card("Mystical Elf")
    assert type(monster.play_from_hand()) == Summon


def test_can_summon_a_monster():
    monster = find_card("Mystical Elf")

    field_half = FieldHalf([monster])
    field_half = field_half.draw()

    abstract_field = AbstractField(
        active_player=field_half, inactive_player=FieldHalf([])
    )
    game_state, abstract_field = monster.play_from_hand().apply(
        GameState(), abstract_field
    )

    assert abstract_field.active_player.monsterAt(Zone.First) == monster
    assert abstract_field.active_player.numberOfCards() == 0


def test_cannot_summon_if_zone_is_not_empty():
    monster = find_card("Mystical Elf")

    field_half = FieldHalf([monster, monster, monster, monster, monster, monster])
    field_half = field_half.draw(6)
    abstract_field = AbstractField(
        active_player=field_half, inactive_player=FieldHalf([])
    )

    # Fill all 5 zones
    for i in range(1, 6):
        game_state, abstract_field = monster.play_from_hand().apply(
            GameState(), abstract_field
        )

    with raises(SummoningError):
        monster.play_from_hand().apply(GameState(), abstract_field)


def test_can_only_normal_summon_once_per_turn():
    monster = find_card("Mystical Elf")

    game_state = GameState()
    field_half = FieldHalf([monster, monster])
    field_half = field_half.draw(2)
    abstract_field = AbstractField(
        active_player=field_half, inactive_player=FieldHalf([])
    )
    game_state, abstract_field = monster.play_from_hand().apply(
        game_state, abstract_field
    )

    with raises(SummoningError):
        game_state, abstract_field = monster.play_from_hand().apply(
            game_state, abstract_field
        )
