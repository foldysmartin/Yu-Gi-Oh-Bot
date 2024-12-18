from pytest import raises
from Field import Field
from abstract_field import Zone
from cards import find_card
from effects import Destroy
from empty_space import EmptySpace
from field_half import FieldHalf
from game_state import GameState
from invalid_target_error import InvalidTargetError


def test_active_monster_is_destroyed():
    monster = find_card("Mystical Elf")
    active = FieldHalf(deck=[], hand=[], monsters=[monster])
    inactive = FieldHalf(deck=[], hand=[], monsters=[])
    field = Field(active_player=active, inactive_player=inactive)
    game_state = GameState()

    game_state, field = Destroy(id=monster.instance_id).apply(game_state, field)
    assert field.active_player.monsterAt(Zone.First) == EmptySpace()


def test_inactive_monster_is_destroyed():
    monster = find_card("Mystical Elf")
    active = FieldHalf(deck=[], hand=[], monsters=[])
    inactive = FieldHalf(deck=[], hand=[], monsters=[monster])
    field = Field(active_player=active, inactive_player=inactive)
    game_state = GameState()

    game_state, field = Destroy(id=monster.instance_id).apply(game_state, field)
    assert field.inactive_player.monsterAt(Zone.First) == EmptySpace()


def test_throw_error_if_monster_not_found():
    monster = find_card("Mystical Elf")
    active = FieldHalf(deck=[], hand=[], monsters=[])
    inactive = FieldHalf(deck=[], hand=[], monsters=[])
    field = Field(active_player=active, inactive_player=inactive)
    game_state = GameState()

    with raises(InvalidTargetError):
        game_state, field = Destroy(id=monster.instance_id).apply(game_state, field)
