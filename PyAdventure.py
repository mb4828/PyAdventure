from game.TestRoom import TestRoom
from engine.utils import ANSIColors


class PyAdventure:
    def __init__(self):
        self.main()

    def main(self):
        print(f"{ANSIColors.GREEN}{ANSIColors.BOLD}{ANSIColors.UNDERLINE}PY ADVENTURE{ANSIColors.ENDC}\n")
        print("A text adventure game prototype developed by Matt Brauner")
        print("(c) Copyright 2022\n")
        print(f"Instructions: Type commands into the prompter to complete the adventure. Available verbs are: "
              f"{ANSIColors.BLUE} LOOK AT, PICK UP, USE, PUSH, PULL {ANSIColors.ENDC}\n")
        TestRoom()


if __name__ == '__main__':
    PyAdventure()
