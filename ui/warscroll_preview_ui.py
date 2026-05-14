from __future__ import annotations

from collections import defaultdict
from typing import Any

from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import HTML, AnyFormattedText, FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VerticalAlign, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Frame, Label

from infrastructure.warscroll import WarscrollDict, Warscrolls, WarscrollsDict
from ui.screen import Screen, ScreenName


class WarscrollsPreviewMenu(Screen):
    """Preview screen for browsing warscrolls in a master/detail layout."""

    def __init__(self, warscroll_path: str):
        self.path = warscroll_path
        self.selected_warscroll_key: str | None = None
        self._warscrolls: WarscrollsDict = {}
        self._ordered_keys: list[str] = []
        self._selected_index: int = 0

    def show(self) -> ScreenName:
        warscrolls = Warscrolls.load_warscrolls(self.path)
        if not warscrolls:
            self.selected_warscroll_key = None
            return ScreenName.MANAGE_ARMIES

        self._warscrolls = warscrolls
        self._ordered_keys = self._build_ordered_keys(warscrolls)
        self._selected_index = 0
        self.selected_warscroll_key = self._get_current_key()

        list_window = self._create_list_window()
        details_window = self._create_details_window()
        root_container = self._create_root_container(list_window, details_window)

        app = Application(
            layout=Layout(root_container, focused_element=list_window),
            key_bindings=self._create_app_key_bindings(),
            style=self._create_style(),
            full_screen=False,
            mouse_support=False,
        )
        app.run()

        return ScreenName.MANAGE_ARMIES

    def _build_ordered_keys(self, warscrolls: WarscrollsDict) -> list[str]:
        return sorted(
            warscrolls,
            key=lambda key: (
                self._get_warscroll_type_label(warscrolls[key]).lower(),
                warscrolls[key]["name"].lower(),
            ),
        )

    def _get_warscroll_type_label(self, warscroll: WarscrollDict) -> str:
        warscroll_type = warscroll.get("type", "").strip()
        return warscroll_type or "Uncategorized"

    def _get_grouped_keys(self) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = defaultdict(list)
        for key in self._ordered_keys:
            grouped[self._get_warscroll_type_label(self._warscrolls[key])].append(key)
        return dict(grouped)

    def _get_current_key(self) -> str:
        return self._ordered_keys[self._selected_index]

    def _get_current_warscroll(self) -> WarscrollDict:
        return self._warscrolls[self._get_current_key()]

    def _create_list_window(self) -> Window:
        return Window(
            content=FormattedTextControl(
                self._get_list_text,
                key_bindings=self._create_list_key_bindings(),
                focusable=True,
                show_cursor=False,
            ),
            wrap_lines=False,
            dont_extend_height=False,
            always_hide_cursor=True,
        )

    def _create_details_window(self) -> Window:
        return Window(
            content=FormattedTextControl(self._get_detail_text),
            wrap_lines=True,
            dont_extend_height=False,
            always_hide_cursor=True,
        )

    def _create_root_container(
        self, list_window: Window, details_window: Window
    ) -> HSplit:
        return HSplit(
            [
                Box(
                    Label(
                        text=HTML("<u>Select a Warscroll:</u>"),
                        dont_extend_height=True,
                    ),
                    padding_left=1,
                    padding_right=1,
                ),
                VSplit(
                    [
                        Box(
                            Frame(list_window, title="Warscrolls"),
                            padding_left=1,
                            padding_right=1,
                            width=Dimension(min=28, preferred=36, weight=1),
                        ),
                        Box(
                            Frame(details_window, title="Details"),
                            padding_right=1,
                            width=Dimension(min=60, weight=3),
                        ),
                    ],
                    padding=1,
                    height=Dimension(min=12, weight=1),
                ),
                Window(height=1, char=" "),
                Box(
                    Label(
                        text=[
                            (
                                "class:help",
                                "Use ↑/↓ to browse, Enter to select, Esc to go back.",
                            )
                        ],
                        dont_extend_height=True,
                    ),
                    padding_left=1,
                    padding_right=1,
                    padding_top=1,
                ),
            ],
            align=VerticalAlign.TOP,
        )

    def _create_list_key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("up")
        @kb.add("k")
        def _move_up(event) -> None:
            self._move_selection(-1)
            event.app.invalidate()

        @kb.add("down")
        @kb.add("j")
        def _move_down(event) -> None:
            self._move_selection(1)
            event.app.invalidate()

        @kb.add("home")
        def _move_home(event) -> None:
            self._selected_index = 0
            self.selected_warscroll_key = self._get_current_key()
            event.app.invalidate()

        @kb.add("end")
        def _move_end(event) -> None:
            self._selected_index = len(self._ordered_keys) - 1
            self.selected_warscroll_key = self._get_current_key()
            event.app.invalidate()

        @kb.add("pageup")
        def _page_up(event) -> None:
            self._move_selection(-5)
            event.app.invalidate()

        @kb.add("pagedown")
        def _page_down(event) -> None:
            self._move_selection(5)
            event.app.invalidate()

        return kb

    def _create_app_key_bindings(self) -> KeyBindings:
        kb = KeyBindings()

        @kb.add("enter", eager=True)
        def _accept(event) -> None:
            self.selected_warscroll_key = self._get_current_key()
            event.app.exit(result=self.selected_warscroll_key)

        @kb.add("escape", eager=True)
        @kb.add("c-c", eager=True)
        def _cancel(event) -> None:
            self.selected_warscroll_key = None
            event.app.exit(result=None)

        return kb

    def _move_selection(self, step: int) -> None:
        next_index = self._selected_index + step
        self._selected_index = min(max(next_index, 0), len(self._ordered_keys) - 1)
        self.selected_warscroll_key = self._get_current_key()

    def _get_list_text(self) -> AnyFormattedText:
        fragments: list[tuple[str, str]] = []

        for group_name, keys in self._get_grouped_keys().items():
            if fragments:
                fragments.append(("", "\n"))

            fragments.append(("class:list.group", f"{group_name}\n"))

            for key in keys:
                warscroll = self._warscrolls[key]
                is_selected = key == self._get_current_key()
                item_style = (
                    "class:list.item.selected" if is_selected else "class:list.item"
                )
                meta_style = (
                    "class:list.meta.selected" if is_selected else "class:list.meta"
                )
                hero_style = (
                    "class:list.hero.selected" if is_selected else "class:list.hero"
                )
                prefix = "> " if is_selected else "  "

                if is_selected:
                    fragments.append(("[SetCursorPosition]", ""))

                fragments.append((item_style, prefix + warscroll["name"]))
                if warscroll["is_hero"]:
                    fragments.append((hero_style, " (Hero)"))
                fragments.append((meta_style, f" — {warscroll['points']} pts"))
                fragments.append(("", "\n"))

        return FormattedText(fragments)

    def _get_detail_text(self) -> AnyFormattedText:
        warscroll = self._get_current_warscroll()
        fragments: list[tuple[str, str]] = []

        fragments.append(("class:detail.title", warscroll["name"]))
        if warscroll["is_hero"]:
            fragments.append(("class:detail.hero", " (Hero)"))
        fragments.append(("", "\n"))

        summary_bits = [
            self._get_warscroll_type_label(warscroll),
            "Hero" if warscroll["is_hero"] else "Non-Hero",
            f"{warscroll['points']} points",
        ]
        fragments.append(("class:detail.meta", " • ".join(summary_bits)))
        fragments.append(("", "\n\n"))

        description = warscroll.get("descr", "").strip() or "No description available."
        self._append_text_section(fragments, "Description", description)

        profile_lines = self._build_profile_lines(warscroll)
        self._append_field_section(fragments, "Profile", profile_lines)

        regiment_options = warscroll.get("regiment_options", [])
        if regiment_options:
            self._append_collection_section(
                fragments, "Regiment Options", regiment_options
            )

        keywords = warscroll.get("keywords", [])
        if keywords:
            self._append_text_section(
                fragments, "Keywords", ", ".join(str(keyword) for keyword in keywords)
            )

        abilities = warscroll.get("abilities", {})
        if abilities:
            self._append_collection_section(fragments, "Abilities", abilities)

        weapons = warscroll.get("weapons", {})
        if weapons:
            self._append_collection_section(fragments, "Weapons", weapons)

        self._append_additional_sections(fragments, warscroll)

        return FormattedText(fragments)

    def _build_profile_lines(self, warscroll: WarscrollDict) -> list[tuple[str, str]]:
        lines = [
            ("Type", self._get_warscroll_type_label(warscroll)),
            ("Hero", "Yes" if warscroll["is_hero"] else "No"),
            ("Points", str(warscroll["points"])),
        ]

        optional_fields = [
            ("Move", warscroll.get("move", "")),
            ("Save", warscroll.get("save", "")),
            ("Control", warscroll.get("control", "")),
            ("Health", warscroll.get("health", "")),
            (
                "Unit Size",
                str(warscroll.get("unit_size", ""))
                if warscroll.get("unit_size")
                else "",
            ),
            ("Base Size", warscroll.get("base_size", "")),
            (
                "Reinforce",
                "Yes" if warscroll.get("can_be_reinforced") else "No",
            ),
        ]

        for label, value in optional_fields:
            if str(value).strip():
                lines.append((label, str(value)))

        return lines

    def _append_additional_sections(
        self, fragments: list[tuple[str, str]], warscroll: WarscrollDict
    ) -> None:
        additional_fields: list[tuple[str, str]] = []

        for key, value in warscroll.items():
            if key in self._handled_detail_keys() or not self._has_display_value(value):
                continue

            title = self._humanize_label(key)

            if isinstance(value, (dict, list)):
                self._append_collection_section(fragments, title, value)
                continue

            formatted_value = self._format_scalar_value(value)
            if "\n" in formatted_value or len(formatted_value) > 100:
                self._append_text_section(fragments, title, formatted_value)
            else:
                additional_fields.append((title, formatted_value))

        if additional_fields:
            self._append_field_section(
                fragments, "Additional Details", additional_fields
            )

    @staticmethod
    def _handled_detail_keys() -> set[str]:
        return {
            "name",
            "type",
            "descr",
            "points",
            "is_hero",
            "move",
            "save",
            "control",
            "health",
            "unit_size",
            "base_size",
            "can_be_reinforced",
            "regiment_options",
            "keywords",
            "abilities",
            "weapons",
        }

    @staticmethod
    def _has_display_value(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (list, dict, tuple, set)):
            return len(value) > 0
        return True

    @staticmethod
    def _format_scalar_value(value: Any) -> str:
        if isinstance(value, bool):
            return "Yes" if value else "No"
        return str(value)

    def _append_text_section(
        self, fragments: list[tuple[str, str]], title: str, value: str
    ) -> None:
        self._append_section_title(fragments, title)
        fragments.append(("class:detail.value", value))
        fragments.append(("", "\n\n"))

    def _append_field_section(
        self,
        fragments: list[tuple[str, str]],
        title: str,
        lines: list[tuple[str, str]],
    ) -> None:
        if not lines:
            return

        self._append_section_title(fragments, title)
        for label, value in lines:
            fragments.append(("class:detail.label", f"{label}: "))
            fragments.append(("class:detail.value", f"{value}\n"))
        fragments.append(("", "\n"))

    def _append_collection_section(
        self,
        fragments: list[tuple[str, str]],
        title: str,
        value: dict[str, Any] | list[Any],
    ) -> None:
        if not value:
            return

        self._append_section_title(fragments, title)
        self._append_nested_value(fragments, value, indent=0)
        fragments.append(("", "\n"))

    def _append_nested_value(
        self,
        fragments: list[tuple[str, str]],
        value: dict[str, Any] | list[Any] | Any,
        indent: int,
        label: str | None = None,
    ) -> None:
        prefix = " " * indent

        if isinstance(value, dict):
            if label is not None:
                fragments.append(
                    (
                        "class:detail.subheading",
                        f"{prefix}{self._humanize_label(label)}\n",
                    )
                )
                prefix = " " * (indent + 2)
                indent += 2

            for child_label, child_value in value.items():
                self._append_nested_value(
                    fragments, child_value, indent=indent, label=child_label
                )
            return

        if isinstance(value, list):
            if label is not None:
                fragments.append(
                    (
                        "class:detail.subheading",
                        f"{prefix}{self._humanize_label(label)}\n",
                    )
                )
                indent += 2
                prefix = " " * indent

            for item in value:
                if isinstance(item, (dict, list)):
                    fragments.append(("class:detail.value", f"{prefix}-\n"))
                    self._append_nested_value(fragments, item, indent=indent + 2)
                else:
                    fragments.append(("class:detail.value", f"{prefix}- {item}\n"))
            return

        if label is None:
            fragments.append(("class:detail.value", f"{prefix}{value}\n"))
            return

        fragments.append(
            ("class:detail.label", f"{prefix}{self._humanize_label(label)}: ")
        )
        fragments.append(("class:detail.value", f"{value}\n"))

    def _append_section_title(
        self, fragments: list[tuple[str, str]], title: str
    ) -> None:
        fragments.append(("class:detail.section", f"{title}\n"))

    @staticmethod
    def _humanize_label(label: str) -> str:
        return label.replace("_", " ").strip().title()

    @staticmethod
    def _create_style() -> Style:
        return Style.from_dict(
            {
                "frame.border": "fg:#666666",
                "frame.label": "bold",
                "list.group": "bold fg:#a5c261",
                "list.item": "",
                "list.item.selected": "reverse",
                "list.meta": "fg:#888888",
                "list.meta.selected": "reverse",
                "list.hero": "italic fg:#d7af5f",
                "list.hero.selected": "italic reverse",
                "detail.title": "bold",
                "detail.hero": "italic fg:#d7af5f",
                "detail.meta": "fg:#888888",
                "detail.section": "bold underline",
                "detail.subheading": "bold",
                "detail.label": "fg:#5fafd7",
                "detail.value": "",
                "help": "fg:#888888",
            }
        )
