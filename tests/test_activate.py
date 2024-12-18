from pytest import raises
from field_half import FieldHalf, HandEmptyError


def test_cannot_activate_card_if_hand_is_empty():
    field_half = FieldHalf([])

    with raises(HandEmptyError):
        field_half.play_from_hand(1)
