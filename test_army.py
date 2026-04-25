import array
import os
from army import Army
from warscroll import Warscroll
from unit import Unit


TEST_ARMY_PATH = "test_army.json"

army_name = "army_01"
reg_name_01 = "Regiment 00"
reg_name_02 = "Regiment 01"

ws1 = Warscroll("Clanrats", 150, False)
ws2 = Warscroll("Grey Seer", 300, True)

unit_01 = Unit.from_warscroll(ws1)
unit_02 = Unit.from_warscroll(ws2)


def init_army() -> Army:
    return Army(army_name)

def save_two_regiment_army():
    army = init_army()
    army.add_regiment()
    army.add_regiment()
    
    army.regiments[0].add_unit(unit_01)
    army.regiments[0].add_unit(unit_02)
    
    army.regiments[1].add_unit(unit_01)
    army.regiments[1].add_unit(unit_01)
    army.regiments[1].add_unit(unit_02)
    
    army.save_army(TEST_ARMY_PATH)

def delete_army_json_file() -> None:
    if os.path.exists(TEST_ARMY_PATH):
        os.remove(TEST_ARMY_PATH)

def test_army_init():
    army = init_army()

    assert army.name == army_name
    assert army.regiments == []
    assert army._regiment_number == 0

def test_add_regiment():
    army = init_army()

    reg_01 = army.add_regiment()
    
    assert len(army.regiments) == 1
    assert army._regiment_number == 1
    assert army.regiments[0].name == reg_name_01
    assert reg_01.name == reg_name_01

def test_add_multiple_regiments():
    army = init_army()

    reg_01 = army.add_regiment()
    reg_02 = army.add_regiment()

    assert len(army.regiments) == 2
    assert army._regiment_number == 2
    assert reg_01.name == reg_name_01
    assert army.regiments[0].name == reg_name_01
    assert reg_02.name == reg_name_02
    assert army.regiments[1].name == reg_name_02

def test_save_army_with_no_regiments():
    delete_army_json_file()

    army = init_army()
    army.save_army(TEST_ARMY_PATH)
    assert os.path.exists(TEST_ARMY_PATH)

def test_load_army_with_no_regiments():
    # arrange    
    delete_army_json_file()
    saved_army = Army("army_999")
    saved_army.save_army(TEST_ARMY_PATH)

    # act
    army = init_army()
    army.load_army(TEST_ARMY_PATH)
    
    # assert
    assert army.name == "army_999"

    # cleanup
    delete_army_json_file()


def test_save_with_two_regiments():
    # arrange
    delete_army_json_file()
    save_two_regiment_army()

    # assert
    assert os.path.exists(TEST_ARMY_PATH)

    # cleanup
    delete_army_json_file()

def test_load_with_two_regiments():
    # arrange
    delete_army_json_file()
    save_two_regiment_army()

    army = init_army()
    army.load_army(TEST_ARMY_PATH)

    assert army.name == army_name
    assert len(army.regiments) == 2
    
    assert army.regiments[0].units[0].warscroll.name == "Clanrats"
    assert army.regiments[0].units[1].warscroll.name == "Grey Seer"

    assert army.regiments[1].units[0].warscroll.name == "Clanrats"
    assert army.regiments[1].units[1].warscroll.name == "Clanrats"
    assert army.regiments[1].units[2].warscroll.name == "Grey Seer"
