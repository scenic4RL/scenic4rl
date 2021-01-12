import math

from scenic.core.vectors import Vector
from scenic.simulators.gfootball.utilities import translator
#from scenic.simulators.gfootball.utilities.constants import player_code_to_role
from scenic.simulators.gfootball.utilities.constants import RoleCode
from scenic.simulators.gfootball.utilities.translator import get_angle_from_direction


def get_velocity_and_speed(position, position_prev):
    delx = position.x - position_prev.x
    dely = position.y - position_prev.y

    velocity = Vector(delx, dely)
    speed = math.sqrt(delx * delx + dely * dely)

    return velocity, speed


def update_game_state(obs, game_state):
    game_state.frame = obs["frame"]
    game_state.score = obs["score"]
    game_state.steps_left = obs["steps_left"]
    game_state.game_mode = obs["game_mode"]


def is_player(obj):
    strs = ["Player", "CB", "GK", "LB", "RB", "CM", "CML", "CMR", "CMM", "CF", "AM", "LM", "RM", "DM"]
    obj_type_str = str(type(obj))
    for s in strs:
        if s in obj_type_str:
            return True
    return False

def is_my_player(obj):
    if not is_player(obj): return False
    strs = ["MyPlayer", "MyCB", "MyGK", "MyLB", "MyRB", "MyCM", "MyCML", "MyCMR", "MyCMM", "MyCF", "MyAM", "MyLM", "MyRM", "MyDM"]
    obj_type_str = str(type(obj))
    for s in strs:
        if s in obj_type_str:
            return True
    return False

def is_op_player(obj):
    if not is_player(obj): return False
    op_strs = ["OpPlayer", "Op"]
    for s in op_strs:
        if s in str(type(obj)):
            return True
    return False

def is_ball(obj):
    return "Ball" in str(type(obj))

def extract_info_from_single_obs(obs):
    my_player_idx_info_map = {} #idx to info
    op_player_idx_info_map = {}
    ball_info = {}


    team_prefixes = ["left_team", "right_team"]
    player_infos = [my_player_idx_info_map, op_player_idx_info_map]


    ball_owned_team = obs['ball_owned_team']
    ball_owned_player = obs['ball_owned_player']

    for team_prefix, player_info in zip(team_prefixes, player_infos):
        tp = team_prefix
        for idx in range(obs[f'{tp}_roles'].shape[0]):
            pos = obs[tp][idx]
            direction = obs[f"{tp}_direction"][idx]
            tired = obs[f"{tp}_tired_factor"][idx]
            yellows = obs[f"{tp}_yellow_card"][idx]
            active = bool(obs[f"{tp}_active"][idx])
            red_card = not active


            info_map = {}
            player_info[idx] = info_map
            info_map['position'] = translator.pos_sim_to_scenic(pos)
            info_map['position_sim'] = pos

            info_map['direction'] = get_angle_from_direction(direction)
            info_map['direction_sim'] = Vector(direction[0], direction[1])

            info_map['tired_factor'] = tired

            info_map['yellow_cards'] = int(yellows)
            info_map['red_card'] = red_card

            info_map["controlled"] = (obs["active"] == idx)

            info_map["owns_ball"] = False
            ball_own_team_code = 0 if tp == "left_team" else 1
            if ball_owned_team == ball_own_team_code and ball_owned_player == idx:
                info_map["owns_ball"] = True

            info_map["sticky_actions"] = None
            if info_map["controlled"]:
                info_map["sticky_actions"] = list(obs["sticky_actions"])

    return my_player_idx_info_map, op_player_idx_info_map

def get_player_info_from_single_obs(obs):
    """To be able to pair player objects in scenic and observation,
        We add the constraint the every team can have at most one player in the same role"""
    my_player_info = {}
    my_ind_to_role = {}

    op_player_info = {}
    op_ind_to_role = {}

    team_prefixes = ["left_team", "right_team"]
    player_infos = [my_player_info, op_player_info]
    ind_to_roles = [my_ind_to_role, op_ind_to_role]

    ball_owned_team = obs['ball_owned_team']
    ball_owned_player = obs['ball_owned_player']

    # print(obs["active"], obs["designated"])
    # read the left and right team arrays and put information in the corresponding DS
    for team_prefix, player_info, ind_to_role in zip(team_prefixes, player_infos, ind_to_roles):
        tp = team_prefix
        # mirrorx = False if tp=="left_team" else True
        for ind in range(obs[f'{tp}_roles'].shape[0]):
            role_code = obs[f"{tp}_roles"][ind]
            role = RoleCode.code_to_role(role_code)
            ind_to_role[ind] = role

            pos = obs[tp][ind]
            direction = obs[f"{tp}_direction"][ind]
            tired = obs[f"{tp}_tired_factor"][ind]
            yellows = obs[f"{tp}_yellow_card"][ind]
            active = bool(obs[f"{tp}_active"][ind])
            red_card = not active

            player_info[role] = {}
            player_info[role]['position'] = translator.pos_sim_to_scenic(pos)
            player_info[role]['position_sim'] = pos

            player_info[role]['direction'] = get_angle_from_direction(direction)
            player_info[role]['direction_sim'] = Vector(direction[0], direction[1])

            player_info[role]['tired_factor'] = tired

            player_info[role]['yellow_cards'] = int(yellows)
            player_info[role]['red_card'] = red_card

            player_info[role]["controlled"] = (obs["active"] == ind)

            # if tp=="right_team" and role=="GK":
            #    print(f"{tp} {role} position {player_info[role]['pos']} direction {player_info[role]['direction']} {player_info[role]['direction_sim']}")

            player_info[role]["owns_ball"] = False
            ball_own_team_code = 0 if tp == "left_team" else 1
            if ball_owned_team == ball_own_team_code and ball_owned_player == ind:
                player_info[role]["owns_ball"] = True

            player_info[role]["sticky_actions"] = None
            if player_info[role]["controlled"]:
                player_info[role]["sticky_actions"] = list(obs["sticky_actions"])

    return my_player_info, my_ind_to_role, op_player_info, op_ind_to_role

def generate_index_to_player_map(last_obs, objects):
    obs = last_obs[0]
    my_player_idx_info_map, op_player_idx_info_map = extract_info_from_single_obs(obs)
    my_player_to_idx, my_idx_to_player, op_player_to_idx, op_idx_to_player = {}, {}, {}, {}


    for obj in objects:
        if is_player(obj):

            if is_my_player(obj):
                info_map = my_player_idx_info_map
                pos_to_idx = my_player_to_idx
                idx_to_pos = my_idx_to_player

            else:
                info_map = op_player_idx_info_map
                pos_to_idx = op_player_to_idx
                idx_to_pos = op_idx_to_player

            min_distance = None
            min_idx = -1
            for idx, info in info_map.items():
                p = info["position"]
                dist = math.sqrt(math.pow(p.x-obj.position.x, 2) +  math.pow(p.y-obj.position.y, 2))
                if min_distance is None or dist<min_distance:
                    min_idx = idx
                    min_distance = dist

                pos_to_idx[obj] = min_idx
                idx_to_pos[min_idx] = obj

                #print(obj.position, p, idx, dist, min_idx, min_distance)
            #print()

    return my_player_to_idx, my_idx_to_player, op_player_to_idx, op_idx_to_player

def update_objects_from_obs(last_obs, objects, game_state, my_player_to_idx, my_idx_to_player, op_player_to_idx, op_idx_to_player, num_controlled=1):
    obs = last_obs[0]
    #my_player_info, my_ind_to_role, op_player_info, op_ind_to_role = get_player_info_from_single_obs(obs)

    my_player_idx_info_map, op_player_idx_info_map = extract_info_from_single_obs(obs)


    update_game_state(obs, game_state)


    for info, idx_to_player, player_to_idx in zip([my_player_idx_info_map, op_player_idx_info_map],\
                        [my_idx_to_player, op_idx_to_player],\
                        [my_player_to_idx, op_player_to_idx]):

        for idx, obj in idx_to_player.items():
            obj.position_prev = obj.position

            obj.position = info[idx]["position"]
            obj.position_sim = info[idx]["position_sim"]
            obj.direction = info[idx]["direction"]
            obj.direction_sim = info[idx]["direction_sim"]
            obj.tired_factor = info[idx]["tired_factor"]
            obj.red_card = info[idx]["red_card"]
            obj.yellow_cards = info[idx]["yellow_cards"]
            obj.controlled = info[idx]["controlled"]
            obj.owns_ball = info[idx]["owns_ball"]

            obj.velocity, obj.speed = get_velocity_and_speed(obj.position, obj.position_prev)

            if not hasattr(obj, "sticky_actions") or obj.sticky_actions is None:
                obj.sticky_actions = []

            if info[idx]["sticky_actions"] is not None:
                obj.sticky_actions = info[idx]["sticky_actions"]



    #update_players and Ball
    for obj in objects:
        if "Ball" in str(type(obj)):
            update_ball(obj, obs)


def update_ball(ball, obs):
    #https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
    #5 gfootball states: postion, direction, rotation, owned_team, ownded_player

    ball.position_raw = obs['ball']

    if not hasattr(ball, "position") or ball.position is None:
        ball.position_prev = translator.pos_sim_to_scenic(obs['ball'])
    else:
        ball.position_prev = ball.position

    ball.position = translator.pos_sim_to_scenic(obs['ball'])


    ball.direction_raw = obs["ball_direction"]
    ball.direction = translator.get_angle_from_direction(obs["ball_direction"])
    ball.heading = ball.direction

    ball.rotation = obs["ball_rotation"]
    ball.owned_team = obs['ball_owned_team']
    ball.owned_player_idx = obs['ball_owned_player']

    #scenic related properties




    delx = ball.position.x - ball.position_prev.x
    dely = ball.position.y - ball.position_prev.y

    velocity1 = Vector(delx, dely)
    speed1 = math.sqrt(delx*delx + dely*dely)

    ball.velocity, ball.speed = get_velocity_and_speed(ball.position, ball.position_prev)

    #print(ball.velocity, ball.speed)
    """
    ball_info = {}
    ball_info["direction"] = obs['ball_direction']
    ball_info["ball_rotation"] = obs['ball_rotation']
    ball_info["ball_owned_team"] = obs['ball_owned_team']
    ball_info["ball_owned_player"] = obs['ball_owned_player']
    ball_info["pos"] = translator.pos_sim_to_scenic(obs['ball'])
    """

def get_scenario_python_str(scene_attrs, own_players, opo_players, ball):
    code_str = ""
    code_str += "from . import *\n"

    code_str += "def build_scenario(builder):\n"

    # basic settings:
    for name, value in scene_attrs.items():
        value_str = f"{value}"
        if isinstance(value, str): value_str = f"'{value_str}'"
        code_str += f"\tbuilder.config().{name} = {value_str}\n"

    code_str += f"\n"
    # add Ball
    ball_pos_sim = translator.pos_scenic_to_sim(ball.position)
    code_str += f"\tbuilder.SetBallPosition({ball_pos_sim.x}, {ball_pos_sim.y})\n"

    code_str += f"\n"

    # addOwnPlayers:
    if len(own_players ) >0:
        code_str += f"\tbuilder.SetTeam(Team.e_Left)\n"
        from scenic.simulators.gfootball.utilities.constants import RoleCode
        for player in own_players:
            player_pos_sim = translator.pos_scenic_to_sim(player.position)
            code_str += f"\tbuilder.AddPlayer({player_pos_sim.x}, {player_pos_sim.y}, e_PlayerRole_{player.role})\n"

        code_str += "\n"
        code_str += "\n"

    # addOponentPlayers:
    if len(opo_players ) >0:
        code_str += f"\tbuilder.SetTeam(Team.e_Right)\n"

        for player in opo_players:
            player_pos_sim = translator.pos_scenic_to_sim(player.position, mirrorx=True)
            #MIRRORING the position of the opponent player, as it seems the simulator mirrors it automatically
            code_str += f"\tbuilder.AddPlayer({player_pos_sim.x}, {player_pos_sim.y}, e_PlayerRole_{player.role})\n"

        code_str += "\n"
        code_str += "\n"

    return code_str