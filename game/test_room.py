from engine.adventure_object import AdventureObject
from engine.adventure_room import AdventureRoom
from engine.utils import AdventureAction


class Cell(AdventureObject):
    def on_lookat(self) -> None:
        text = f"You {'awake' if self.check_state('is_first_look') else 'are'} in a cell containing a bed, a table, and a barred door with a {'smashed ' if not self.check_state('is_door_locked') else ''}lock on it \n"

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
        if self.check_state('is_brick_hidden'):
            self.on_unknown()
        elif use_with is self.room.rope:
            self.do_output("You smash the rope with the brick, but it doesn't budge. That thing is solid")
        elif use_with is self.room.ring:
            self.do_output("You smash the ring with the brick. Some rusty metal flies off, but the ring is still intact")
        elif self.check_state('is_rope_attached'):
            self.do_output("The rope around your ankle becomes snug. You can't reach it")
        elif use_with is self.room.door:
            self.do_output("You smash the door with the brick, but it doesn't budge. That thing is solid")
        elif use_with is self.room.lock:
            self.do_output("You smash the lock with the brick, breaking it open. Freedom?")
            self.set_state('is_door_locked', False)
        else:
            self.do_output('Nothing happens')


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

    def on_use(self, use_with=None):
        if use_with is None:
            self.on_pickup()
        elif use_with is self.room.rope:
            self.do_output("The rope is too thick to cut with the dagger")
        elif use_with is self.room.ring:
            self.do_output("The ring is too thick to cut with the dagger")
        elif use_with is self.room.door:
            self.do_output("The door is too thick to cut with the dagger")
        elif use_with is self.room.lock:
            self.do_output("The lock is too thick to cut with the dagger")
        elif use_with is self.room.pillow:
            self.do_output("The dagger cuts through the pillow, hitting something hard inside")
        elif use_with is self.room.mattress:
            self.do_output("The dagger cuts through the mattress, but doesn't seem to do anything")
        else:
            self.do_output("Nothing happens")


class Lock(AdventureObject):
    def on_lookat(self):
        if self.check_state('is_door_locked'):
            self.do_output("It's locked")
        else:
            self.do_output("The lock is smashed to pieces")
            self.set_state('is_door_locked', False)

    def on_pickup(self):
        self.on_lookat()

    def on_push(self):
        self.on_lookat()

    def on_pull(self):
        self.on_lookat()

    def on_use(self, use_with=None):
        self.on_lookat()

class Door(AdventureObject):
    def on_lookat(self):
        if self.check_state('is_door_locked'):
            self.do_output("It's a sturdy, metal door with a lock on it")
        else:
            self.do_output("It's a sturdy, metal door with a broken lock on it")

    def on_pickup(self):
        self.on_lookat()

    def on_push(self):
        if self.check_state('is_rope_attached'):
            self.do_output("The rope around your ankle becomes snug. You can't reach it")
        elif not self.check_state('is_door_locked') and not self.check_state('is_door_oiled'):
            self.do_output("The door won't budge")
        elif self.check_state('is_door_locked') and self.check_state('is_door_oiled'):
            self.do_output("The door opens and you escape to freedom!")
            self.set_state('is_door_open', True)
        else:
            self.do_output("The door won't budge. What gives?")

    def on_pull(self):
        self.on_push()

    def on_use(self, use_with=None):
        self.on_push()


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
        self.lock = Lock(self, ['lock', 'keyhole'])
        self.door = Door(self, ['door', 'entrance', 'exit'])
        super().__init__()

        self.cell.on_lookat()
        self.state.set('is_first_look', False)

        while self.state.get('is_door_open') is False:
            (action, objects) = self.parser.wait_for_input()
            if len(objects) == 1:
                objects[0].perform_action(action)
            elif len(objects) == 2 and action is AdventureAction.USE:
                objects[0].perform_action(action, objects[1])
            else:
                self.cell.on_unknown()