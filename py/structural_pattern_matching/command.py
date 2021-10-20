

def main():
    while True:

        command = input("input a command: ").split()
        match command:
            case ["move", direction]:
                print(f"move to {direction}")
            case ["attack", target, skill]:
                print(f"attack to {target} by {skill}")
            case ["home"]:
                print(f"go back home ......")
            case ["message", *contents]:
                print(f"{contents}")
            case ["exit", *_]:
                print("Good bye!")
                return
            case _:
                print("====invalid command====")


if __name__ == "__main__":
    main()
