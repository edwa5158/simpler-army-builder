from infrastructure.warscroll import Warscrolls, WarscrollsDict


def warscroll_selection():
    warscrolls: WarscrollsDict = Warscrolls.load_warscrolls()

    for warscroll in warscrolls:
        print(warscroll)


if __name__ == "__main__":
    print("Hello, there!")
    warscroll_selection()
