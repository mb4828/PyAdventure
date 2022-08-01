from engine import AdventureObjectInterface
from engine.Inventory import Inventory
from engine.TextParser import TextParser


class AdventureRoomInterface:
    """
    Interface representing a room that the player can visit and interact with objects within
    """

    """ Parser for the room """
    parser = None

    """ Player inventory """
    inventory = None

    """ Holds state variables for the room """
    state = {}

    def __init__(self, inventory=None):
        self.parser = TextParser(self.get_all_objects_in_room())
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = Inventory()

    def get_all_objects_in_room(self) -> list[AdventureObjectInterface]:
        """
        Extracts all objects in the room into a list to be passed into the parser
        """
        results = []
        for attr in dir(self):
            obj = getattr(self, attr)
            if isinstance(obj, AdventureObjectInterface.AdventureObjectInterface):
                results.append(obj)
        return results

    def output_inventory_contents(self) -> None:
        """
        Outputs everything in inventory for the player to see
        """
        self.parser.do_output(f"Inventory: {map(lambda i: i.keywords[0] + ', ', self.inventory.inventory)}")

    def use_object_with_object(self, obj1: AdventureObjectInterface, obj2: AdventureObjectInterface) -> None:
        """
        Takes two objects and invokes use action
        """
        pass
