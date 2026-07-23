from typing import cast

from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput

from infrastructure.warscroll import WarscrollDict
from ui.warscroll_preview_ui import WarscrollsPreviewMenu


def build_preview_menu(warscroll: WarscrollDict) -> WarscrollsPreviewMenu:
    menu = WarscrollsPreviewMenu("data/test_warscroll.json")
    menu._warscrolls = {warscroll["name"]: warscroll}
    menu._ordered_keys = [warscroll["name"]]
    menu._selected_index = 0
    menu.selected_warscroll_key = warscroll["name"]
    return menu


def render_detail_text(menu: WarscrollsPreviewMenu) -> str:
    return "".join(
        fragment[1] for fragment in to_formatted_text(menu._get_detail_text())
    )


def test_preview_detail_shows_all_profile_fields_and_empty_sections():
    warscroll = cast(
        WarscrollDict,
        {
            "name": "Test Unit",
            "type": "Infantry",
            "descr": "",
            "points": 120,
            "is_hero": False,
            "move": "",
            "save": "",
            "control": "",
            "health": "",
            "unit_size": 0,
            "base_size": "",
            "can_be_reinforced": False,
            "regiment_options": [],
            "abilities": {},
            "keywords": [],
            "weapons": {},
        },
    )

    text = render_detail_text(build_preview_menu(warscroll))

    assert "Move: —" in text
    assert "Save: —" in text
    assert "Control: —" in text
    assert "Health: —" in text
    assert "Unit Size: —" in text
    assert "Base Size: —" in text
    assert "Can Be Reinforced: No" in text
    assert "Regiment Options\n—" in text
    assert "Keywords\n—" in text
    assert "Abilities\n—" in text
    assert "Weapons\n—" in text


def test_preview_detail_shows_populated_collection_fields():
    warscroll = cast(
        WarscrollDict,
        {
            "name": "Grey Seer",
            "type": "Infantry Hero",
            "descr": "Masterclan spellcaster.",
            "points": 300,
            "is_hero": True,
            "move": '6"',
            "save": "6+",
            "control": "2",
            "health": "5",
            "unit_size": 1,
            "base_size": "32mm",
            "can_be_reinforced": False,
            "regiment_options": ["Any Skaven"],
            "abilities": {
                "Warpstone Shards": {
                    "Description": "Enhance the next cast.",
                    "Effect": "Roll 3D6 instead of 2D6.",
                }
            },
            "keywords": ["Hero", "Wizard(1)", "Skaven"],
            "weapons": {
                "melee_weapons": {
                    "Warpstone Staff": {
                        "Attack": "3",
                        "Hit": "4+",
                    }
                }
            },
        },
    )

    text = render_detail_text(build_preview_menu(warscroll))

    assert "Regiment Options" in text
    assert "- Any Skaven" in text
    assert "Keywords" in text
    assert "- Hero" in text
    assert "- Wizard(1)" in text
    assert "Abilities" in text
    assert "Warpstone Shards" in text
    assert "Effect: Roll 3D6 instead of 2D6." in text
    assert "Weapons" in text
    assert "Warpstone Staff" in text
    assert "Attack: 3" in text
    assert "Can Be Reinforced: No" in text


def test_preview_detail_arrow_key_scroll_works_after_tab_focus():
    warscroll = cast(
        WarscrollDict,
        {
            "name": "Clanrats",
            "type": "Infantry",
            "descr": (
                "Clanrats are the unwashed masses of the Clans Verminus. "
                "No matter how many are cut down, the tide never seems to slacken."
            ),
            "points": 150,
            "is_hero": False,
            "move": '6"',
            "save": "5+",
            "control": "1",
            "health": "1",
            "unit_size": 20,
            "base_size": "25mm",
            "can_be_reinforced": True,
            "regiment_options": [],
            "abilities": {
                "Seething Swarm": {
                    "Description": "Overwhelm the enemy with numbers.",
                    "Effect": "Return D3 slain models to this unit.",
                }
            },
            "keywords": [
                "Infantry",
                "Champion",
                "Musician (1/20), Standard Bearer (1/20)",
                "Chaos",
                "Skaven",
                "Verminus",
            ],
            "weapons": {
                "melee_weapons": {
                    "Rusty Weapon": {
                        "Attack": "2",
                        "Hit": "4+",
                        "Wound": "5+",
                        "Rend": "-",
                        "Damage": "1",
                        "Weapon Abilities": ["Crit (Auto-wound)"],
                    }
                }
            },
        },
    )
    menu = build_preview_menu(warscroll)

    with create_pipe_input() as pipe_input:
        pipe_input.send_text("\t")
        pipe_input.send_bytes(b"\x1b[B")
        pipe_input.send_text("\x03")

        app = menu._build_application(input=pipe_input, output=DummyOutput())
        app.run()

    assert menu._focused_panel == "Details"
    assert menu._details_pane is not None
    assert menu._details_pane.vertical_scroll > 0
