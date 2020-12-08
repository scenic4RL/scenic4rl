from gfootball.env import football_action_set
from scenic.core.vectors import Vector
from scenic.core.simulators import Action

from scenic.simulators.gfootball.utilities.constants import ActionCode

class SetDirection(Action):
    def __init__(self, direction: int):
        self.direction = direction
        self.code = direction

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return f"direction {self.direction}"

class Shoot(Action):
    def __init__(self):
        self.code = 12

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "shoot"

class NoAction(Action):
    def __init__(self):
        self.code = 0

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "no action"

class Sliding(Action):
    def __init__(self):
        self.code = ActionCode.sliding

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "sliding"