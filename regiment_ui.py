from __future__ import annotations

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from tabulate import tabulate

from army import ArmiesDict, Army, army_file_contents, army_file_exists
from config import ARMY_PATH


def list_regiments(army: Army):
    print("\n")
    for regiment in army.regiments:
        print(regiment.regiment_header())
        print("-" * 75)
        for unit in regiment.units:
            print(unit.unit.unit_row())
        print("\n")


def regiment_menu() -> None:
    pass


def main() -> None:
    pass


if __name__ == "__main__":
    main()
