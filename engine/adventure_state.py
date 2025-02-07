class AdventureState:
    """
    State controller which holds state variables
    """
    __state = {
        'is_first_look': True,
        'is_rope_attached': True,
        'is_dagger_stuck': True,
        'is_brick_hidden': True,
        'is_door_locked': True,
        'is_door_oiled': False,
        'is_door_open': False
    }

    def get(self, key):
        return self.__state[key]

    def set(self, key, val):
        self.__state[key] = val
