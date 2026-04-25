from typing import Callable
class Option:
    def __init__(
        self,
        description: str = "",
        func: Callable = lambda: None,
        args: tuple = (),
        kwargs: dict = {},
    ):
        self.description = description
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}


def prompt_user(options: dict[int, Option]) -> tuple[int, str]:
    """
    options {
        key [int]: Option
    }
    """
    if 0 in options:
        raise ValueError("Cannot allow '0' as an option")

    # Build input prompt
    answer: int = 0
    prompt = "Select an option:\n\t"
    prompt += "\n\t".join(
        [f"{key}. {option.description}" for key, option in options.items()]
    )
    prompt += "\n"

    # Wait for valid response
    while answer not in options:
        answer_in = input(prompt)
        try:
            answer = int(answer_in)
        except ValueError:
            answer = 0
        if answer not in options:
            print("Invalid option. Please try again.")

    # Take action, return answer
    option = options.get(answer, Option())
    option.func(*option.args, **option.kwargs)

    return (answer, option.description)
