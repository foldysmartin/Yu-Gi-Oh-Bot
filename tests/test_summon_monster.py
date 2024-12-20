from pytest import raises
from empty_space import EmptySpace
from field_half import FieldHalf, Zone
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

    field_half = FieldHalf(deck=[], hand=[monster], monsters=[monster])
    abstract_field = AbstractField(
        active_player=field_half, inactive_player=FieldHalf([])
    )

    with raises(SummoningError):
        monster.play_from_hand().apply(GameState(), abstract_field)


def test_can_only_normal_summon_once_per_turn():
    monster = find_card("Mystical Elf")

    game_state = GameState()
    field_half = FieldHalf(deck=[], hand=[monster, monster])
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


def test_can_only_normal_summon_in_main_phase():
    game_state = GameState()
    assert game_state.can_normal_summon() == True

    game_state = game_state.change_phase()
    assert game_state.can_normal_summon() == False

    game_state = game_state.change_phase()
    assert game_state.can_normal_summon() == True
