from warscroll import get_user_inputs, new_warscroll,save_warscrolls
import pytest
from pytest import MonkeyPatch
import sys
import io

name: str = "Clanrats"
points: int = 150
is_hero: bool = False
input_tuple = (name, points, is_hero)
warscroll_dict = {"name": name, "points": points, "is_hero": is_hero}

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
    from pathlib import Path
    assert Path("warscrolls.json").exists()