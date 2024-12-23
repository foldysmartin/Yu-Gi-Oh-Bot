from pytest import raises
from abstract_field import AbstractField, AbstractFieldHalf, Zone
from cards.load_card import find_card
from game_state import GameState
from summoning.normal.to_normal_summon import ToNormalSummon


def test_to_nornmal_summon():
    monster = find_card("Mystical Elf")
    game_state = GameState()
    field = AbstractField(
        AbstractFieldHalf(deck=[], hand=[monster]), AbstractFieldHalf(deck=[])
    )

    summon_action = ToNormalSummon(index=0)

    effect = summon_action.activate(field, game_state)
    field, game_state = effect.apply(field, game_state)

    assert field.active_player.monsterAt(Zone.First) == monster
    assert field.active_player.numberOfCards() == 0


def test_multiple_nornmal_summons():
    monster1 = find_card("Mystical Elf")
    monster2 = find_card("Mystical Elf")
    field = AbstractField(
        AbstractFieldHalf(deck=[], hand=[monster1, monster2]),
        AbstractFieldHalf(deck=[]),
    )

    summon_action = ToNormalSummon(index=0)

    effect = summon_action.activate(field, GameState())
    field, _ = effect.apply(field, GameState())

    effect = summon_action.activate(field, GameState())
    field, _ = effect.apply(field, GameState())

    assert field.active_player.monsterAt(Zone.First) == monster1
    assert field.active_player.monsterAt(Zone.Second) == monster2
    assert field.active_player.numberOfCards() == 0


def test_can_only_have_5_monsters():
    monster1 = find_card("Mystical Elf")
    monster2 = find_card("Mystical Elf")
    game_state = GameState()
    field = AbstractField(
        AbstractFieldHalf(
            deck=[],
            hand=[monster1],
            monsters=[monster2, monster2, monster2, monster2, monster2],
        ),
        AbstractFieldHalf(deck=[]),
    )

    with raises(Exception):
        summon_action = ToNormalSummon(index=0)
        effect = summon_action.activate(field, game_state)
        field, game_state = effect.apply(field, game_state)


def test_can_only_summon_once_per_turn():
    monster1 = find_card("Mystical Elf")
    monster2 = find_card("Mystical Elf")
    game_state = GameState()
    field = AbstractField(
        AbstractFieldHalf(deck=[], hand=[monster1, monster2]),
        AbstractFieldHalf(deck=[]),
    )

    summon_action = ToNormalSummon(index=0)
    effect = summon_action.activate(field, game_state)
    field, game_state = effect.apply(field, game_state)

    with raises(Exception):
        summon_action = ToNormalSummon(index=0)
        effect = summon_action.activate(field, game_state)
        field, game_state = effect.apply(field, game_state)


def test_can_only_summon_in_normal_phases():
    monster = find_card("Mystical Elf")
    game_state = GameState(phase="battle")
    field = AbstractField(
        AbstractFieldHalf(deck=[], hand=[monster]),
        AbstractFieldHalf(deck=[]),
    )

    with raises(Exception):
        summon_action = ToNormalSummon(index=0)
        effect = summon_action.activate(field, game_state)
        field, game_state = effect.apply(field, game_state)
