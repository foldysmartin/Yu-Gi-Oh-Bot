from cards import find_card
from monster_card import MonsterCard


def test_normal_monster_card():
    mystical_elf = find_card("Mystical Elf")
    assert mystical_elf.attack == 800
    assert mystical_elf.defence == 2000
    assert mystical_elf.level == 4
    assert mystical_elf.name == "Mystical Elf"


def test_uuids_are_different():
    mystical_elf = find_card("Mystical Elf")
    mystical_elf_2 = find_card("Mystical Elf")
    assert mystical_elf.instance_id != mystical_elf_2.instance_id
