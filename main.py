from new_army import new_army

def main():
    options = {
        1: "New Army",
        2: "Load Army",
        3: "Exit"
    }
    answer: int = 0
    input_text = "Select an option (1-3):\n\t"
    input_text += "\n\t".join([f"{key}. {value}" for key, value in options.items()])
    input_text += "\n"

    while answer not in options.keys():
        answer = input(input_text)

        try:
            answer = int(answer)
        except ValueError:
            answer = 0
        if answer not in options.keys():
            print("Invalid option. Please try again.")
    
    match answer:
        case 1:
            new_army()
        case 2:
            print("You selected LOAD ARMY")
        case 3:
            print("Exiting...")


if __name__ == "__main__":
    main()