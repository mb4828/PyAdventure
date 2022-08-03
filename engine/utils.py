from enum import Enum

class AdventureAction(Enum):
    """ Actions the player can perform """
    UNKNOWN = 0
    LOOK_AT = 1
    PICK_UP = 2
    USE = 3
    PUSH = 4
    PULL = 5


class ANSIColors:
    """ Colors to make the command line look less crappy """
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    GRAY = '\033'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'