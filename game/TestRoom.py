from engine.AdventureObjectInterface import AdventureObjectInterface
from engine.AdventureRoomInterface import AdventureRoomInterface


class Cell(AdventureObjectInterface):
    def on_lookat(self) -> None:
        text = f"You {'awake' if self.check_state('is_first_look') else 'are'} in a cell containing a bed, a table, and a barred door with a lock on it.\n"

        text += "On the bed is a flimsy, thatched mattress, an uncomfortable-looking pillow, and a copy of `Arr and `Arr magazine.\n"

        if not self.check_state('is_brick_hidden') and not self.room.inventory.has_object(Brick):
            text += "A heavy brick on the floor near the foot of the bed\n"

        if self.check_state('is_rope_attached'):
            text += "A sturdy rope is secured around your ankle, connecting to a metal ring that's screwed into the bed frame.\n"
        else:
            text += "A sturdy rope is secured around your ankle, the metal ring it was once attached to now a pile of rusty metal.\n"

        if self.check_state('is_dagger_stuck'):
            text += 'Across the room, a rusty dagger stands upright, jammed into the center of a wooden table'
        else:
            text += 'Across the room, there is a wooden table with nothing on it'

        self.set_state('is_first_look', False)
        self.do_output(text)


class Bed(AdventureObjectInterface):
    pass


class Fish(AdventureObjectInterface):
    pass


class Oil(AdventureObjectInterface):
    pass


class Pillow(AdventureObjectInterface):
    def on_lookat(self):
        if self.check_state('is_brick_hidden'):
            self.do_output("It's an uncomfortable-looking pillow")
        else:
            self.do_output("It's an uncomfortable-looking empty pillowcase")

    def on_pickup(self):
        if self.check_state('is_brick_hidden'):
            self.do_output("As you pick the pillow up, a heavy brick falls out. No wonder it was so uncomfortable!")
            self.set_state('is_brick_hidden', False)
        elif self.in_inventory():
            self.do_output("The pillow is in your inventory")
        else:
            self.do_output("Pillow added to inventory")
            self.add_to_inventory()

    def on_push(self):
        if self.check_state('is_brick_hidden'):
            self.do_output("It's an uncomfortable-looking, heavy pillow")
        else:
            self.do_output("Nothing happens")

    def on_pull(self):
        self.on_push()


class Brick(AdventureObjectInterface):
    def on_lookat(self):
        if self.check_state('is_brick_hidden'):
            self.on_unknown()
        else:
            self.do_output("It's a heavy brick")

    def on_pickup(self):
        if self.check_state('is_brick_hidden'):
            self.on_unknown()
        else:
            self.do_output("Brick has been added to your inventory")
            self.room.inventory.add_object(self)

    def on_use(self, use_with):
        # TODO
        pass


class Magazine(AdventureObjectInterface):
    pass


class Rope(AdventureObjectInterface):
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


class Ring(AdventureObjectInterface):
    def on_lookat(self):
        if self.check_state('is_rope_attached'):
            self.do_output("It's a rusty, metal ring with a rope securely attached to it")
        else:
            self.do_output("It's a broken metal ring with nothing attached to it")

    def on_pickup(self):
        self.do_output("The ring is screwed into the bed frame and can't be picked up")

    def on_pull(self):
        if self.check_state('is_rope_attached'):
            self.do_output("The rust gives out, and the metal ring crumbles, freeing the rope and your ankle. Guess it wasn't so secure after all!")
            self.set_state('is_rope_attached', False)
        else:
            self.do_output("Nothing happens")

    def on_push(self):
        self.on_pull()


class Table(AdventureObjectInterface):
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


class Dagger(AdventureObjectInterface):
    def on_lookat(self):
        self.do_output("It's a rusty, old dagger")

    def on_pickup(self):
        if self.check_state('is_rope_attached'):
            self.do_output("You reach for the dagger but the rope around your ankle prevents you from reaching it")
        elif self.in_inventory():
            self.do_output("The dagger is in your inventory")
        else:
            self.do_output("Dagger has been added to your inventory")
            self.add_to_inventory()
            self.set_state('is_dagger_stuck', False)


class Lock(AdventureObjectInterface):
    def on_lookat(self):
        if self.check_state('is_door_locked'):
            self.do_output("It's locked")


class Inv(AdventureObjectInterface):
    def on_lookat(self):
        self.room.output_inventory_contents()


class TestRoom(AdventureRoomInterface):
    state = {
        'is_first_look': True,
        'is_rope_attached': True,
        'is_dagger_stuck': True,
        'is_brick_hidden': True,
        'is_door_locked': True
    }

    def __init__(self):
        self.cell = Cell(self, ['cell', 'room'])
        self.bed = Bed(self, ['bed', 'mattress'])
        self.fish = Fish(self, ['fish', 'can', 'food'])
        self.oil = Oil(self, ['oil', 'grease'])
        self.pillow = Pillow(self, ['pillow'])
        self.brick = Brick(self, ['brick', 'stone', 'rock'])
        self.magazine = Magazine(self, ['magazine', 'book'])
        self.rope = Rope(self, ['rope', 'cord', 'knot', 'tie'])
        self.ring = Ring(self, ['ring', 'metal'])
        self.table = Table(self, ['table'])
        self.dagger = Dagger(self, ['dagger', 'blade', 'knife'])
        self.lock = Lock(self, ['lock', 'door'])
        self.inv = Inv(self, ['inventory'])
        super().__init__()

        self.cell.on_lookat()
        while self.state['is_door_locked'] is True:
            (action, objects) = self.parser.wait_for_input()
            if len(objects) is 0:
                self.parser.do_output("Could not parse command")
            else:
                for obj in objects:
                    obj.perform_action(action)


