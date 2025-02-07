class AdventureInventory:
    """
    Inventory controller which holds the state of the player's inventory
    """
    __inventory: list = []

    def add_object(self, obj) -> None:
        """ Adds an object to the player's inventory """
        self.__inventory.append(obj)

    def remove_object(self, obj) -> None:
        """ Removes an object from the player's inventory """
        for i in self.__inventory:
            if type(i) is type(obj):
                self.__inventory.remove(i)

    def has_object(self, obj) -> bool:
        """ Returns a boolean indicating whether the player has an object in inventory """
        for i in self.__inventory:
            if type(i) is type(obj):
                return True
        return False

    def get_all(self):
        """ Returns everything in inventory """
        return self.__inventory
