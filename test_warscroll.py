import os

from config import WARSCROLL_PATH
from shared import delete_file_if_it_exists
from warscroll import Warscroll, Warscrolls
from pprint import pformat

ws1 = Warscroll("Clanrats", 150, False)
ws2 = Warscroll("Grey Seer", 300, True)
ws3 = Warscroll("Ratling Gun", 200, False)


def warscrolls_setup() -> Warscrolls:
    warscrolls = Warscrolls()
    warscrolls.append_warscroll(ws1)
    warscrolls.append_warscroll(ws2)
    warscrolls.append_warscroll(ws3)
    return warscrolls


def test_warscrolls_save():
    # arrange
    delete_file_if_it_exists(WARSCROLL_PATH)
    warscrolls = warscrolls_setup()
    # act
    warscrolls.save_warscrolls()
    # assert
    assert os.path.exists(WARSCROLL_PATH)
    # cleanup
    delete_file_if_it_exists(WARSCROLL_PATH)


def test_warscrolls_load():
    # arrange
    delete_file_if_it_exists(WARSCROLL_PATH)
    warscrolls = warscrolls_setup()
    warscrolls.save_warscrolls()

    #act
    new_warscrolls = Warscrolls.load_warscrolls()

    # assert
    assert len(new_warscrolls) == len(warscrolls.catalog)
    assert new_warscrolls == warscrolls.serialized_catalog

    # cleanup
    delete_file_if_it_exists(WARSCROLL_PATH)

def test_warscrolls_load_with_no_file():
    # arrange
    delete_file_if_it_exists(WARSCROLL_PATH)

    #act
    warscrolls = Warscrolls.load_warscrolls()

    # assert
    assert warscrolls == {}

    # cleanup
    delete_file_if_it_exists(WARSCROLL_PATH)

def test_print_warscrolls_prints_serialized_catalog(capsys):
    warscrolls = warscrolls_setup()
    warscrolls.print_warscrolls()

    captured = capsys.readouterr()

    assert captured.out == pformat(warscrolls.serialized_catalog) + "\n"
    assert captured.err == "" 