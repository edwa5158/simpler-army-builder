from warscroll import Warscroll, Warscrolls


def warscroll_selection():
    warscrolls: dict[str, Warscroll] = Warscrolls.load_warscrolls()

    for warscroll in warscrolls:
        print(warscroll)


if __name__ == "__main__":
    print("Hello, there!")
    warscroll_selection()
