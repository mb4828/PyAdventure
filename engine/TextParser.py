import re

from engine import AdventureObjectInterface
from utils import AdventureAction, ANSIColors


class TextParser:
    """
    Text parser used for parsing player input
    """

    LOOK_SYNONYMS = ["look", "view", "examine", "study", "observe", "sight", "see"]
    PICKUP_SYNONYMS = ["pick", "take", "grab", "collect", "gather"]
    USE_SYNONYMS = ["use", "put"]
    PUSH_SYNONYMS = ["push", "shove", "press", "bump", "knock", "ram", "jolt", "prod", "hit"]
    PULL_SYNONYMS = ["pull", "tug", "draw", "heave", "lug", "jerk", "twist", "pry", "yank"]

    objects: list[AdventureObjectInterface] = []

    def __init__(self, objects: list[AdventureObjectInterface]):
        self.objects = objects

    def __parse_action(self, user_input: list[str]) -> AdventureAction:
        ui = set(user_input)
        if not set(self.LOOK_SYNONYMS).isdisjoint(ui):
            return AdventureAction.LOOK_AT
        if not set(self.PICKUP_SYNONYMS).isdisjoint(ui):
            return AdventureAction.PICK_UP
        if not set(self.USE_SYNONYMS).isdisjoint(ui):
            return AdventureAction.USE
        if not set(self.PUSH_SYNONYMS).isdisjoint(ui):
            return AdventureAction.PUSH
        if not set(self.PULL_SYNONYMS).isdisjoint(ui):
            return AdventureAction.PULL
        return AdventureAction.UNKNOWN

    def __parse_objects(self, user_input: list[str]) -> list[AdventureObjectInterface]:
        ui = set(user_input)
        objs = []
        for obj in self.objects:
            keywords = map(lambda k: k.lower(), obj.keywords)
            if not ui.isdisjoint(keywords):
                objs.append(obj)
        return objs

    def wait_for_input(self) -> (AdventureAction, list[AdventureObjectInterface]):
        """
        Waits for input from the player and returns the parsed object and action
        """
        user_input = input("> ").lower().split(" ")
        return self.__parse_action(user_input), self.__parse_objects(user_input)

    def do_output(self, s: str):
        """
        Handles the output of the user's action. In this case - just printing some text
        Any object that is mentioned is automatically highlighted for the user!
        """
        result = []
        for word in s.split(" "):
            clean_word = re.sub('\\W', '', word)
            found_word = False
            for obj in self.objects:
                if not found_word and re.search(f" {clean_word} ", f" {' '.join(obj.keywords)} ", re.IGNORECASE):
                    found_word = True
                    result.append(f"{ANSIColors.BLUE}{word.upper()}{ANSIColors.ENDC}")
                    break
            if not found_word:
                result.append(word)
        print(' '.join(result))

