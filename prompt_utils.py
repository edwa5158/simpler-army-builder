class Option:
    def __init__(
        self,
        description: str = "",
        func: callable = None,
        args: tuple = None,
        kwargs: dict = None,
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
    if 0 in options.keys():
        raise ValueError("Cannot allow '0' as an option")

    # Build input prompt
    answer: int = 0
    input_text = "Select an option:\n\t"
    input_text += "\n\t".join(
        [f"{key}. {option.description}" for key, option in options.items()]
    )
    input_text += "\n"

    # Wait for valid response
    while answer not in options.keys():
        answer = input(input_text)
        try:
            answer = int(answer)
        except ValueError:
            answer = 0
        if answer not in options.keys():
            print("Invalid option. Please try again.")

    # Take action, return answer
    option = options.get(answer, Option())
    option.func(*option.args, **option.kwargs)

    return (answer, option.description)
