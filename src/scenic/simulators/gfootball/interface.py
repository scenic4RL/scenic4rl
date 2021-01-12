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


def update_objects_from_obs(last_obs, objects, game_state):
    obs = last_obs[0]
    update_game_state(obs, game_state)

    ball_owned_team = obs['ball_owned_team']
    ball_owned_player = obs['ball_owned_player']

    """To be able to pair player objects in scenic and observation, 
    We add the constraint the every team can have at most one player in the same role"""
    my_player_info = {}
    my_ind_to_role = {}

    op_player_info = {}
    op_ind_to_role = {}

    team_prefixes = ["left_team", "right_team"]
    player_infos = [my_player_info, op_player_info]
    ind_to_roles = [my_ind_to_role, op_ind_to_role]

    print(obs["active"], obs["designated"])
    #read the left and right team arrays and put information in the corresponding DS
    for team_prefix, player_info, ind_to_role  in zip(team_prefixes, player_infos, ind_to_roles):
        tp = team_prefix
        #mirrorx = False if tp=="left_team" else True
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
            ball_own_team_code = 0 if tp=="left_team" else 1
            if ball_owned_team == ball_own_team_code and ball_owned_player == ind:
                player_info[role]["owns_ball"] = True

            player_info[role]["sticky_actions"] = None
            if player_info[role]["controlled"]:
                player_info[role]["sticky_actions"] = list(obs["sticky_actions"])



    for obj in objects:


        if is_player(obj):

            my_player=True
            info = my_player_info
            mirrorx=False


            if is_op_player(obj):
                info = op_player_info
                my_player = False
                mirrorx = True


            #TODO test if the right side teams x locations are reported correctly

            role = obj.role

            obj.position_prev = obj.position



            obj.position = info[role]["position"]
            obj.position_sim = info[role]["position_sim"]
            obj.direction = info[role]["direction"]
            obj.direction_sim = info[role]["direction_sim"]
            obj.tired_factor = info[role]["tired_factor"]
            obj.red_card = info[role]["red_card"]
            obj.yellow_cards = info[role]["yellow_cards"]
            obj.controlled = info[role]["controlled"]
            obj.owns_ball = info[role]["owns_ball"]

            obj.velocity, obj.speed = get_velocity_and_speed(obj.position, obj.position_prev)

            if not hasattr(obj, "sticky_actions") or obj.sticky_actions is None:
                obj.sticky_actions = []

            if info[role]["sticky_actions"] is not None:
                obj.sticky_actions = info[role]["sticky_actions"]


        elif "Ball" in str(type(obj)):
            update_ball(obj, obs)

            #print(f"Ball {obj.position} with {obj.direction} degree {obs['ball_direction']}")


    x=1

def update_player():
    pass
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