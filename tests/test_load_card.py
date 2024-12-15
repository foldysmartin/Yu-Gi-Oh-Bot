from cards import find_card
from monster_card import MonsterCard


def test_normal_monster_card():
    mystical_elf = MonsterCard(name="Mystical Elf", attack=800, defence=2000, level=4)
    assert mystical_elf == find_card("Mystical Elf")