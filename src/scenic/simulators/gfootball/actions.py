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
    def __init__(self, pass_type="short"):
        print("pass action: ", pass_type)
        allowed_type = {"long":9, "high":10, "short":11}
        assert pass_type in allowed_type
        self.code = allowed_type[pass_type]

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

class Dribble(Action):
    def __init__(self):
        self.code = constants.ActionCode.dribble

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "dribble"

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

class ReleaseDribble(Action):
    def __init__(self):
        self.code = constants.ActionCode.release_dribble

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "release dribble"

class ReleaseSprint(Action):
    def __init__(self):
        self.code = constants.ActionCode.release_sprint

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "release sprint"

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

class Slide(Action):
    def __init__(self):
        self.code = ActionCode.sliding

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "slide"

class MoveTowardsPoint(Action):
    '''
    Move Towards given point. Will calculate correct heading for you.
    '''
    # def __init__(self, x, y, self_x, self_y, opponent = False):
    def __init__(self, destination_point, player_position, opponent = False):

        self_x = player_position.x
        self_y = player_position.y
        x = destination_point.x
        y = destination_point.y

        if opponent:
            corresponding_dir = lookup_direction(self_x - x, self_y - y)
        else:
            corresponding_dir = lookup_direction(x - self_x, y - self_y)

        self.code = corresponding_dir

    def applyTo(self, obj, sim):
        pass

    def __str__(self):
        return "MoveTowardsPoint {}, {}, op={}".format(self.x, self.y, self.opponent)

# ------Helper Functions------
def lookup_direction(dx, dy):
    # direction is [0,360] with 0/360 = North clockwise
    direction = math.atan2(dx, dy) * 180 / math.pi
    if direction < 0:
        direction += 360

    # print("direction: ", direction)

    # lookup action based on direction
    action_lookup = [3, 4, 5, 6, 7, 8, 1, 2, 3]
    corresponding_dir = action_lookup[round(direction / 40) % 9]
    return corresponding_dir


def player_with_ball(ds, ball, team=None):
    """
    Return the player with ball. Use team=0,1 to specify team
    @param ds:
    @param ball:
    @param team: 0 or 1
    @return:
    """
    assert (team is None) or (team in (0,1))
    if (team is not None) and (team != ball.owned_team):
        return None

    if (ball.owned_team == 0):
        return ds.my_players[ball.owned_player_idx]
    if (ball.owned_team == 1):
        return ds.op_players[ball.owned_player_idx]
    return None

def get_closest_player_dis(position, players):
    min_distance = None
    closest_player = None

    for p in players:
        dist = math.sqrt(math.pow(p.x - position[0], 2) + math.pow(p.y - position[1], 2))
        if dist == 0:
            continue
        if min_distance is None or dist < min_distance:
            closest_player = p
            min_distance = dist
    return closest_player, min_distance