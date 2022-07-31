class AdventureObjectInterface:
    """
    Interface representing an object that the player can interact with
    """

    """
    List of keywords associated with this object, to be used for text parsing
    """
    keywords = []

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
