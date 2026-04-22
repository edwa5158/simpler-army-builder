from warscroll import get_user_inputs, new_warscroll,save_warscrolls
from pytest import MonkeyPatch
import io
from pathlib import Path
import os

if Path("warscrolls.json").exists():
    os.remove("filename.txt")

name: str = "Clanrats"
points: int = 150
is_hero: bool = False
input_tuple = (name, points, is_hero)
warscroll_dict = {"name": name, "points": points, "is_hero": is_hero}
warscrolls_json = """{["Clanrats": {"name": "Clanrats", "points": 150, "is_hero": false}]}"""

ratling_warscroll: dict = {"name": "Ratling Gun", "points": 200, "is_hero": False}
filename = "warscrolls.json"

def test_get_user_inputs(monkeypatch: MonkeyPatch):
    mock_args:str = ", ".join([str(x) for x in input_tuple])
    print(mock_args)
    # mock_args = "Clanrats, 150, False"
    monkeypatch.setattr("sys.stdin", io.StringIO(mock_args))
    result = get_user_inputs()

    assert isinstance(result, tuple)
    assert result == input_tuple

def test_new_warscroll():
    result = new_warscroll(name, points, is_hero)

    assert isinstance(result, dict)
    assert result == warscroll_dict

def test_save_warscroll():
    save_warscrolls(warscroll_dict)

    assert Path(filename).exists()
    if Path(filename).exists():
        os.remove(filename)


def test_save_multiple_warscrolls():
    save_warscrolls(warscroll_dict)
    save_warscrolls(ratling_warscroll)


    if Path(filename).exists():
        os.remove(filename)
