from engine.adventure_object import AdventureObject
from engine.adventure_room import AdventureRoom
from engine.utils import AdventureAction


class Cell(AdventureObject):
    def on_lookat(self) -> None:
        text = f"You {'awake' if self.check_state('is_first_look') else 'are'} in a cell containing a bed, a table, and a barred door with a lock on it \n"

        text += "On the bed is a flimsy, thatched mattress, an uncomfortable-looking pillow, and a copy of `Arr and `Arr magazine \n"

        if not self.check_state('is_brick_hidden') and not self.in_inventory(Brick):
            text += "A heavy brick sits on the floor near the head of the bed\n"

        if self.check_state('is_rope_attached'):
            text += "A sturdy rope is secured around your ankle, connecting to a metal ring that's screwed into the bed frame \n"
        else:
            text += "A sturdy rope is secured around your ankle, the metal ring it was once attached to now a pile of rusty metal \n"

        if self.check_state('is_dagger_stuck'):
            text += 'Across the room, a rusty dagger stands upright, jammed into the center of a wooden table'
        else:
            text += 'Across the room, there is a wooden table with nothing on it'

        self.do_output(text)


class Bed(AdventureObject):
    def on_lookat(self) -> None:
        if self.check_state('is_rope_attached'):
            self.do_output(
                "It's your standard, everyday prison bed. A rusty, metal ring is screwed into the bed frame")
        else:
            self.do_output("It's your standard, everyday prison bed")

    def on_pickup(self):
        self.do_output("The bed is too heavy to move")

    def on_push(self):
        self.on_pickup()

    def on_pull(self):
        self.on_pickup()


class Mattress(AdventureObject):
    pass


class Fish(AdventureObject):
    pass


class Oil(AdventureObject):
    pass


class Pillow(AdventureObject):
    def on_lookat(self):
        if self.check_state('is_brick_hidden'):
            self.do_output("It's an uncomfortable-looking pillow")
        else:
            self.do_output("It's an uncomfortable-looking empty pillowcase")

    def on_pickup(self):
        if self.check_state('is_brick_hidden'):
            self.do_output(
                "As you pick the pillow up, a heavy brick falls out. No wonder it was so uncomfortable!")
            self.set_state('is_brick_hidden', False)
        else:
            self.add_to_inventory()

    def on_push(self):
        if self.check_state('is_brick_hidden'):
            self.do_output("It's an uncomfortable-looking, heavy pillow")
        else:
            self.do_output("Nothing happens")

    def on_pull(self):
        self.on_push()


class Brick(AdventureObject):
    def on_lookat(self):
        if self.check_state('is_brick_hidden'):
            self.on_unknown()
        else:
            self.do_output("It's a heavy brick")

    def on_pickup(self):
        if self.check_state('is_brick_hidden'):
            self.on_unknown()
        else:
            self.add_to_inventory()

    def on_use(self, use_with):
        # TODO
        pass


class Magazine(AdventureObject):
    def on_lookat(self):
        self.do_output("It's a magazine with a picture of a pirate drinking a piña colada on the cover")

    def on_pickup(self):
        self.add_to_inventory()

    def on_use(self, use_with):
        # TODO
        pass


class Rope(AdventureObject):
    def on_lookat(self):
        if self.check_state('is_rope_attached'):
            self.do_output("It's a sturdy rope tied around your ankle and the metal ring")
        else:
            self.do_output("The rope is still tied around your ankle, but it's no longer secured to the metal ring")

    def on_pickup(self):
        self.do_output("The rope is tied around your ankle and can't be picked up")

    def on_pull(self):
        self.do_output("Nothing happens. That's one sturdy rope")

    def on_push(self):
        self.on_pull()


class Ring(AdventureObject):
    def on_lookat(self):
        if self.check_state('is_rope_attached'):
            self.do_output(
                "It's a rusty, metal ring with a rope securely attached to it")
        else:
            self.do_output(
                "It's a broken metal ring with nothing attached to it")

    def on_pickup(self):
        self.do_output(
            "The ring is screwed into the bed frame and can't be picked up")

    def on_pull(self):
        if self.check_state('is_rope_attached'):
            self.do_output(
                "The rusted metal gives out and the ring crumbles, freeing the rope and your ankle. Guess it wasn't so secure after all")
            self.set_state('is_rope_attached', False)
        else:
            self.do_output("Nothing happens")

    def on_push(self):
        self.on_pull()


class Table(AdventureObject):
    def on_lookat(self) -> None:
        if self.check_state('is_dagger_stuck'):
            self.do_output("It's a table with a dagger stuck in it")
        else:
            self.do_output("It's a table with nothing on it")

    def on_pickup(self):
        self.do_output("The table is firmly bolted to the floor")

    def on_push(self):
        self.on_pickup()

    def on_pull(self):
        self.on_pickup()


class Dagger(AdventureObject):
    def on_lookat(self):
        self.do_output("It's a rusty, old dagger")

    def on_pickup(self):
        if self.check_state('is_rope_attached'):
            self.do_output(
                "The dagger is across the room... and the rope around your ankle prevents you from reaching it")
        else:
            self.add_to_inventory()
            self.set_state('is_dagger_stuck', False)


class Lock(AdventureObject):
    def on_lookat(self):
        if self.check_state('is_door_locked'):
            self.do_output("It's locked")

    def on_pickup(self):
        self.on_lookat()

    def on_push(self):
        self.on_lookat()

    def on_pull(self):
        self.on_lookat()


class TestRoom(AdventureRoom):
    def __init__(self):
        self.cell = Cell(self, ['cell', 'room', 'around'])
        self.bed = Bed(self, ['bed'])
        self.mattress = Mattress(self, ['mattress'])
        self.fish = Fish(self, ['fish', 'can', 'food'])
        self.oil = Oil(self, ['oil', 'grease'])
        self.pillow = Pillow(self, ['pillow'])
        self.brick = Brick(self, ['brick', 'stone', 'rock'])
        self.magazine = Magazine(self, ['magazine', 'book'])
        self.rope = Rope(self, ['rope', 'chain', 'cord', 'knot', 'tie'])
        self.ring = Ring(self, ['ring', 'metal'])
        self.table = Table(self, ['table'])
        self.dagger = Dagger(self, ['dagger', 'blade', 'knife'])
        self.lock = Lock(self, ['lock', 'door'])
        super().__init__()

        self.cell.on_lookat()
        self.state.set('is_first_look', False)

        while self.state.get('is_door_locked') is True:
            (action, objects) = self.parser.wait_for_input()
            if len(objects) is 0:
                self.cell.on_unknown()
            else:
                for obj in objects:
                    obj.perform_action(action)
