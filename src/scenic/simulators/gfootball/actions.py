from gfootball.env import football_action_set
from scenic.core.vectors import Vector
from scenic.core.simulators import Action
from scenic.simulators.gfootball.utilities import constants

from scenic.simulators.gfootball.utilities.constants import ActionCode
import math


class SetDirection(Action):
    def __init__(self, direction: int):
        self.direction = direction
        self.code = direction

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return f"direction {self.direction}"

class Pass(Action):
    def __init__(self, type="short"):
        allowed_type = {"long":9, "short":11, "high":10}
        assert type in allowed_type
        self.code = allowed_type[type]

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "pass"


class Shoot(Action):
    def __init__(self):
        self.code = constants.ActionCode.shot

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "shoot"

class Sprint(Action):
    def __init__(self):
        self.code = constants.ActionCode.sprint

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "sprint"

class ReleaseDirection(Action):
    def __init__(self):
        self.code = constants.ActionCode.release_direction

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "release Direction"

class NoAction(Action):
    def __init__(self):
        self.code = 0

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "no action"

class BuiltinAIAction(Action):
    def __init__(self):
        self.code = ActionCode.builtin_ai

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "Built-in AI"

class Sliding(Action):
    def __init__(self):
        self.code = ActionCode.sliding

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "sliding"



# ------Helper Functions------
def lookup_direction(dx, dy):
    # direction is [0,360] with 0/360 = North clockwise
    direction = math.atan2(dx, dy) * 180 / math.pi
    if direction < 0:
        direction += 360

    # lookup action based on direction
    action_lookup = [3, 4, 5, 6, 7, 8, 1, 2, 3]
    corresponding_dir = action_lookup[round(direction / 45)]
    return corresponding_dir
