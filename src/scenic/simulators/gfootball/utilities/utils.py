import math


def is_player(obj):
    strs = ["Player", "CB", "GK", "LB", "RB", "CM", "CML", "CMR", "CMM", "CF", "AM", "LM", "RM", "DM"]
    obj_type_str = str(type(obj))
    for s in strs:
        if s in obj_type_str:
            return True
    return False


def is_my_player(obj):
    if not is_player(obj): return False
    strs = ["LeftPlayer", "LeftCB", "LeftGK", "LeftLB", "LeftRB", "LeftCM", "LeftCML", "LeftCMR", "LeftCMM", "LeftCF", "LeftAM", "LeftLM", "LeftRM", "LeftDM"]
    obj_type_str = str(type(obj))
    for s in strs:
        if s in obj_type_str:
            return True
    return False


def is_op_player(obj):
    if not is_player(obj): return False
    op_strs = ["RightPlayer", "Right"]
    for s in op_strs:
        if s in str(type(obj)):
            return True
    return False


def is_ball(obj):
    return "Ball" in str(type(obj))


def get_closest_player(position, players):
    min_distance = None
    closest_player = None

    for p in players:
        dist = math.sqrt(math.pow(p.x - position[0], 2) + math.pow(p.y - position[1], 2))
        if min_distance is None or dist < min_distance:
            closest_player = p
            min_distance = dist
    return closest_player
