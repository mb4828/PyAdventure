from engine import AdventureObjectInterface


class Inventory:
    """
    Inventory controller which holds the state of the player's inventory
    """
    inventory: list[AdventureObjectInterface] = []

    def add_object(self, obj: AdventureObjectInterface) -> None:
        """
        Adds an object to the player's inventory
        """
        self.inventory.append(obj)

    def remove_object(self, obj: AdventureObjectInterface) -> None:
        """
        Removes an object from the player's inventory
        """
        for i in self.inventory:
            if type(i) is type(obj):
                self.inventory.remove(i)

    def has_object(self, obj: AdventureObjectInterface) -> bool:
        """
        Returns a boolean indicating whether the player has an object in inventory
        """
        # TODO FIX ME!
        for i in self.inventory:
            if type(i) is type(obj):
                return True
        return False

