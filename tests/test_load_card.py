from cards import find_card
from monster_card import MonsterCard


def test_normal_monster_card():
    mystical_elf = MonsterCard(name="Mystical Elf", attack=800, defence=2000, level=4)
    assert mystical_elf == find_card("Mystical Elf")

def test_uuids_are_different():
    mystical_elf = find_card("Mystical Elf")
    mystical_elf_2 = find_card("Mystical Elf")
    assert mystical_elf.instance_id != mystical_elf_2.instance_id