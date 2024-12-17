from pytest import raises
from FieldHalf import FieldHalf, HandEmptyError


def test_cannot_activate_card_if_hand_is_empty():
    field_half = FieldHalf([])

    with raises(HandEmptyError):
        field_half.activate(1)
