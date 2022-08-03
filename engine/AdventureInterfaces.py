from engine.AdventureInventory import AdventureInventory
from engine.TextParser import TextParser
from engine.utils import AdventureAction, ANSIColors


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
        self.do_output(f"{ANSIColors.RED}Could not parse command{ANSIColors.ENDC}")

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
        return self.room.state[state]

    def set_state(self, state, value):
        """ Shortcut method to set state """
        self.room.state[state] = value

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


class AdventureRoom:
    """
    Interface representing a room that the player can visit and interact with objects within
    """

    class InventoryWrapperObject(AdventureObject):
        """ Wrapper for inventory to make it accessible to the player """

        def on_lookat(self):
            self.room.output_inventory_contents()

    """ Parser for the room """
    parser = None

    """ Player inventory """
    inventory = None

    """ Holds state variables for the room """
    state = {}

    def __init__(self, inventory=None):
        if inventory is None:
            inventory = AdventureInventory()
        self.inventory = inventory
        self.__inv = self.InventoryWrapperObject(self, ['inventory', 'inv', 'i'])
        self.parser = TextParser(self.get_all_objects_in_room())

    def get_all_objects_in_room(self) -> list[AdventureObject]:
        """ Extracts all objects in the room into a list to be passed into the parser """
        results = []
        for attr in dir(self):
            obj = getattr(self, attr)
            if isinstance(obj, AdventureObject):
                results.append(obj)
        return results

    def output_inventory_contents(self) -> None:
        """ Outputs everything in inventory for the player to see """
        inv = ', '.join(list(map(lambda i: i.keywords[0], self.inventory.get_all())))
        self.parser.do_output(f"Inventory: {inv}")

    def use_object_with_object(self, obj1: AdventureObject, obj2: AdventureObject) -> None:
        """
        Takes two objects and invokes use action
        """
        pass
