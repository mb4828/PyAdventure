from engine.adventure_object import AdventureObject
from engine.utils import AdventureAction, ANSIColors
import re

class TextParser:
    """
    Text parser used for parsing player input
    """

    LOOK_SYNONYMS = ["look", "lookat", "view", "examine",
                     "study", "observe", "sight", "see", "l"]
    PICKUP_SYNONYMS = ["pick", "pickup", "take",
                       "grab", "collect", "gather", "p"]
    USE_SYNONYMS = ["use", "useon", "put", "with", "u"]
    PUSH_SYNONYMS = ["push", "pushon", "shove", "press",
                     "bump", "knock", "ram", "jolt", "prod", "hit", "s"]
    PULL_SYNONYMS = ["pull", "pullon", "tug", "draw",
                     "heave", "lug", "jerk", "twist", "pry", "yank", "l"]

    objects: list[AdventureObject] = []

    def __init__(self, objects: list[AdventureObject]):
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

    def __parse_objects(self, user_input: list[str]) -> list[AdventureObject]:
        ui = set(user_input)
        objs = []
        for obj in self.objects:
            keywords = map(lambda k: k.lower(), obj.keywords)
            if not ui.isdisjoint(keywords):
                objs.append(obj)
        return objs

    def wait_for_input(self) -> (AdventureAction, list[AdventureObject]):
        """ Waits for input from the player and returns the parsed object and action """
        user_input = input("> ").lower().split(" ")
        return self.__parse_action(user_input), self.__parse_objects(user_input)

    def do_output(self, s: str):
        """
        Handles the output of the user's action. In this case - just printing some text
        Any object that is mentioned is automatically highlighted for the user!
        """
        result = []
        for word in s.split(" "):
            clean_word = re.sub('[^a-zA-Z0-9]', '', word)
            found_word = False
            for obj in self.objects:
                if not found_word and re.search(f" {clean_word} ", f" {' '.join(obj.keywords)} ", re.IGNORECASE):
                    found_word = True
                    result.append(
                        f"{ANSIColors.BLUE}{word.upper()}{ANSIColors.ENDC}")
                    break
            if not found_word:
                result.append(word)
        print(' '.join(result))
