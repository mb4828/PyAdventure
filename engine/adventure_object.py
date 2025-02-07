from engine.utils import AdventureAction
from engine.utils import ANSIColors

class AdventureObject:
    """
    Interface representing an object that the player can interact with
    """

    """ Room that this object is in """
    room = None

    """ List of keywords associated with this object, to be used for text parsing """
    keywords = []

    def __init__(self, room, keywords=[]):
        self.room = room
        self.keywords = keywords

    ### OVERRIDE BELOW METHODS TO IMPLEMENT ACTIONS ###

    def on_lookat(self) -> None:
        """ Logic for when object is looked at """
        self.do_output("Nothing happens")

    def on_pickup(self) -> None:
        """ Logic for when object is picked up """
        self.do_output("Nothing happens")

    def on_use(self, use_with) -> None:
        """ Logic for when object is used """
        self.do_output("Nothing happens")

    def on_push(self) -> None:
        """ Logic for when object is pushed """
        self.do_output("Nothing happens")

    def on_pull(self) -> None:
        """ Logic for when object is pulled """
        self.do_output("Nothing happens")

    def on_unknown(self) -> None:
        self.do_output(
            f"{ANSIColors.RED}Could not parse command{ANSIColors.ENDC}")

    ### HELPER METHODS - DO NOT OVERRIDE ###

    def perform_action(self, action: AdventureAction) -> None:
        """ Performs the desired action by invoking the on_action method """
        if action is AdventureAction.LOOK_AT:
            self.on_lookat()
        elif action is AdventureAction.PICK_UP:
            self.on_pickup()
        elif action is AdventureAction.USE:
            # TODO
            pass
        elif action is AdventureAction.PUSH:
            self.on_push()
        elif action is AdventureAction.PULL:
            self.on_pull()
        else:
            self.on_unknown()

    def check_state(self, state):
        """ Shortcut method to check state """
        return self.room.state.get(state)

    def set_state(self, state, value):
        """ Shortcut method to set state """
        self.room.state.set(state, value)

    def in_inventory(self, obj=None):
        """ Shortcut method to check if an object is in inventory. Pass nothing to check this object """
        if obj is None:
            obj = self
        return self.room.inventory.has_object(obj)

    def add_to_inventory(self, obj=None):
        """ Shortcut method to add an object to inventory. Pass nothing to add this object """
        if obj is None:
            obj = self
        if self.in_inventory(obj):
            self.do_output(f"{obj.keywords[0]} is already in inventory")
        else:
            self.do_output(f"{obj.keywords[0]} added to inventory")
            return self.room.inventory.add_object(obj)

    def do_output(self, output):
        """ Shortcut method to output to parser """
        self.room.parser.do_output(output)
