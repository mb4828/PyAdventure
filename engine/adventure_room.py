from engine.adventure_object import AdventureObject
from engine.adventure_inventory import AdventureInventory
from engine.adventure_state import AdventureState
from engine.text_parser import TextParser


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
    inventory: AdventureInventory = None

    """ Holds state variables for the room """
    state: AdventureState = {}

    def __init__(self, state=None, inventory=None):
        if state is None:
            state = AdventureState()
        self.state = state

        if inventory is None:
            inventory = AdventureInventory()
        self.inventory = inventory
        self.__inv = self.InventoryWrapperObject(
            self, ['inventory', 'inv', 'i'])

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
        inv = ', '.join(
            list(map(lambda i: i.keywords[0], self.inventory.get_all())))
        self.parser.do_output(f"Inventory: {inv}")

    def use_object_with_object(self, obj1: AdventureObject, obj2: AdventureObject) -> None:
        """
        Takes two objects and invokes use action
        """
        pass
