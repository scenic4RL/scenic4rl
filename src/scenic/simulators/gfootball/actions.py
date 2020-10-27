from gfootball.env import football_action_set
from scenic.core.vectors import Vector
from scenic.core.simulators import Action


class SetDirection(Action):
    def __init__(self, direction: int):
        self.direction = direction
        self.code = direction

    def applyTo(self, obj, sim):
        pass


class Shoot(Action):
    def __init__(self):
        self.code = 12

    def applyTo(self, obj, sim):
        pass

class NoAction(Action):
    def __init__(self):
        self.code = 0

    def applyTo(self, obj, sim):
        pass