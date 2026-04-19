from new_army import load_army
from new_army import new_army
from prompt_utils import prompt_user, Option


def main():
    options: dict[int, Option] = {
        1: Option("New Army", new_army),
        2: Option("Load Army", load_army),
        3: Option("Exit", lambda: print("Exiting...")),
    }
    prompt_user(options)


if __name__ == "__main__":
    main()
