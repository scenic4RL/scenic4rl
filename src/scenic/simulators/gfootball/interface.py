from scenic.core.vectors import Vector
from scenic.simulators.gfootball.utilities import translator
#from scenic.simulators.gfootball.utilities.constants import player_code_to_role
from scenic.simulators.gfootball.utilities.constants import RoleCode
from scenic.simulators.gfootball.utilities.translator import get_angle_from_direction


def update_objects_from_obs(last_obs, objects):
    obs = last_obs[0]

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

    #read the left and right team arrays and put information in the corresponding DS
    for team_prefix, player_info, ind_to_role  in zip(team_prefixes, player_infos, ind_to_roles):
        tp = team_prefix
        #mirrorx = False if tp=="left_team" else True
        for ind in range(obs[f'{tp}_roles'].shape[0]):
            role_code = obs[f"{tp}_roles"][ind]
            role = RoleCode.code_to_role(role_code)
            ind_to_role[ind] = role

            # TODO add all from: https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
            pos = obs[tp][ind]
            direction = obs[f"{tp}_direction"][ind]
            tired = obs[f"{tp}_tired_factor"][ind]
            yellows = obs[f"{tp}_yellow_card"][ind]
            red_card = obs[f"{tp}_active"][ind]

            player_info[role] = {}
            player_info[role]['position'] = translator.pos_sim_to_scenic(pos)
            player_info[role]['position_sim'] = pos

            player_info[role]['direction'] = get_angle_from_direction(direction)
            player_info[role]['direction_sim'] = Vector(direction[0], direction[1])

            player_info[role]['tired_factor'] = tired

            if isinstance(yellows, bool): yellows = 0
            player_info[role]['yellow_cards'] = yellows
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

        if "Player" in str(type(obj)):

            my_player=True
            info = my_player_info
            mirrorx=False

            if "OpPlayer" in str(type(obj)):
                info = op_player_info
                my_player = False
                mirrorx = True

            role = obj.role
            obj.position = info[role]["position"]
            obj.position_sim = info[role]["position_sim"]
            obj.direction = info[role]["direction"]
            obj.direction_sim = info[role]["direction_sim"]
            obj.tired_factor = info[role]["tired_factor"]
            obj.red_card = info[role]["red_card"]
            obj.yellow_cards = info[role]["yellow_cards"]
            obj.controlled = info[role]["controlled"]
            obj.owns_ball = info[role]["owns_ball"]

            if not hasattr(obj, "sticky_actions") or obj.sticky_actions is None:
                obj.sticky_actions = []

            if info[role]["sticky_actions"] is not None:
                obj.sticky_actions = info[role]["sticky_actions"]


        elif "Ball" in str(type(obj)):
            update_ball(obj, obs)

            #print(f"Ball {obj.position} with {obj.direction} degree {obs['ball_direction']}")

def update_player():
    pass
def update_ball(ball, obs):
    #https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
    #5 gfootball states: postion, direction, rotation, owned_team, ownded_player
    ball.position_raw = obs['ball']
    ball.position = translator.pos_sim_to_scenic(obs['ball'])

    ball.direction_raw = obs["ball_direction"]
    ball.direction = translator.get_angle_from_direction(obs["ball_direction"])

    ball.rotation = obs["ball_rotation"]
    ball.owned_team = obs['ball_owned_team']
    ball.owned_player_idx = obs['ball_owned_player']

    #scenic related properties



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
        code_str += f"\tbuilder.config().{name} = {value}\n"

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