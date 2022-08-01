from engine import AdventureRoomInterface
from utils import AdventureAction


class AdventureObjectInterface:
    """
    Interface representing an object that the player can interact with
    """

    """ Room that this object is in """
    room: AdventureRoomInterface = None

    """ List of keywords associated with this object, to be used for text parsing """
    keywords = []

    def __init__(self, room: AdventureRoomInterface, keywords=[]):
        self.room = room
        self.keywords = keywords

    ######## OVERRIDE BELOW METHODS TO IMPLEMENT ACTIONS ########

    def on_lookat(self) -> None:
        """
        Logic for when object is looked at
        """
        print("Nothing happens")


    def on_pickup(self) -> None:
        """
        Logic for when object is picked up
        """
        print("Nothing happens")


    def on_use(self, use_with) -> None:
        """
        Logic for when object is used
        """
        print("Nothing happens")

    def on_push(self) -> None:
        """
        Logic for when object is pushed
        """
        print("Nothing happens")


    def on_pull(self) -> None:
        """
        Logic for when object is pulled
        """
        print("Nothing happens")

    def on_unknown(self) -> None:
        print("Could not parse command")

    ######## HELPER METHODS - DO NOT OVERRIDE ########

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
        return self.room.state[state]

    def set_state(self, state, value):
        """ Shortcut method to set state """
        self.room.state[state] = value

    def in_inventory(self):
        """ Shortcut method to check inventory """
        return self.room.inventory.has_object(self)

    def add_to_inventory(self):
        """ Shortcut method to add to inventory """
        return self.room.inventory.add_object(self)

    def do_output(self, output):
        """ Shortcut method to output to parser """
        self.room.parser.do_output(output)
