from scenic.core.vectors import Vector
from scenic.simulators.gfootball.utilities import translator
from scenic.simulators.gfootball.utilities.translator import get_angle_from_direction
from scenic.simulators.gfootball import model

player_code_to_role = {
			0: "GK",
			1: "CB",
			2: "LB",
			3: "RB",
			4: "DM",
			5: "CM",
			6: "LM",
			7: "RM",
			8: "AM",
			9: "CF"
		}

def update_objects_from_obs(last_obs, objects):
    obs = last_obs[0]

    ball_owned_team = obs['ball_owned_team']
    ball_owned_player = obs['ball_owned_player']

    my_player_info = {}
    my_ind_to_role = {}

    op_player_info = {}
    op_ind_to_role = {}

    team_prefixes = ["left_team", "right_team"]
    player_infos = [my_player_info, op_player_info]
    ind_to_roles = [my_ind_to_role, op_ind_to_role]

    for team_prefix, player_info, ind_to_role  in zip(team_prefixes, player_infos, ind_to_roles):
        tp = team_prefix
        for ind in range(obs[f'{tp}_roles'].shape[0]):
            role_code = obs[f"{tp}_roles"][ind]
            role = player_code_to_role[role_code]
            ind_to_role[ind] = role

            # TODO add all from: https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
            pos = obs[tp][ind]
            direction = obs[f"{tp}_direction"][ind]
            tired = obs[f"{tp}_tired_factor"][ind]

            player_info[role] = {}
            player_info[role]['pos'] = translator.pos_sim_to_scenic(pos)
            player_info[role]['pos_sim'] = pos
            player_info[role]['direction'] = get_angle_from_direction(direction)
            player_info[role]['direction_sim'] = Vector(direction[0], direction[1])

            #if tp=="right_team" and role=="GK":
            #    print(f"{tp} {role} position {player_info[role]['pos']} direction {player_info[role]['direction']} {player_info[role]['direction_sim']}")

            player_info[role]['tired'] = tired
            player_info[role]["active"] = obs["active"] == ind
            player_info[role]["ball_owned"] = False

            ball_own_team_code = 0 if tp=="left_team" else 1
            if ball_owned_team == ball_own_team_code and ball_owned_player == ind:
                player_info[role]["ball_owned"] = True

    """
    for ind in range(obs['right_team_roles'].shape[0]):
        role_code = obs["right_team_roles"][ind]
        role = player_code_to_role[role_code]
        op_ind_to_role[ind] = role

        #TODO add all from: https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
        pos = obs["right_team"][ind]
        direction = obs["right_team_direction"][ind]
        tired = obs["right_team_tired_factor"][ind]


        op_player_info[role] = {}
        op_player_info[role]['pos'] = pos
        op_player_info[role]['direction'] = direction
        op_player_info[role]['tired'] = tired
        op_player_info[role]["ball_owned"] = False

        if ball_info["ball_owned_team"] == 1 and ball_info["ball_owned_player"] == ind:
            op_player_info[role]["ball_owned"] = True



    for ind in range(obs['left_team_roles'].shape[0]):
        role_code = obs["left_team_roles"][ind]
        role = player_code_to_role[role_code]
        my_ind_to_role[ind] = role

        #TODO add all from: https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
        pos = obs["left_team"][ind]
        direction = obs["left_team_direction"][ind]
        tired = obs["left_team_tired_factor"][ind]

        my_player_info[role] = {}
        my_player_info[role]['pos'] = pos
        my_player_info[role]['direction'] = direction
        my_player_info[role]['tired'] = tired
        my_player_info[role]["active"] = obs["active"] == ind
        my_player_info[role]["ball_owned"] = False

        if ball_info["ball_owned_team"] == 0 and ball_info["ball_owned_player"] == ind:
            my_player_info[role]["ball_owned"] = True

    """

    """
    ball_info = {}
    ball_info["direction"] = obs['ball_direction']
    ball_info["ball_rotation"] = obs['ball_rotation']
    ball_info["ball_owned_team"] = obs['ball_owned_team']
    ball_info["ball_owned_player"] = obs['ball_owned_player']
    ball_info["pos"] = translator.pos_sim_to_scenic(obs['ball'])
    """
    for obj in objects:

        if "MyPlayer" in str(type(obj)):
            role = obj.role
            obj.position = my_player_info[role]["pos"]
            obj.position_sim = my_player_info[role]["pos_sim"]

            obj.direction = my_player_info[role]["direction"]
            obj.direction_sim = my_player_info[role]["direction_sim"]

            obj.tired = my_player_info[role]["tired"]
            obj.active = my_player_info[role]["active"]
            obj.ball_owned = my_player_info[role]["ball_owned"]


        elif "OpPlayer" in str(type(obj)):
            role = obj.role
            obj.position = op_player_info[role]["pos"]
            obj.tired = op_player_info[role]["tired"]

        elif "Ball" in str(type(obj)):
            obj.position = translator.pos_sim_to_scenic(obs['ball'])
            obj.direction = translator.get_angle_from_direction(obs["ball_direction"])
            obj.owned_team = obs['ball_owned_team']
            obj.owned_player = obs['ball_owned_player']

            #print(f"Ball {obj.position} with {obj.direction} degree {obs['ball_direction']}")



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

        for player in own_players:
            player_pos_sim = translator.pos_scenic_to_sim(player.position)
            code_str += f"\tbuilder.AddPlayer({player_pos_sim.x}, {player_pos_sim.y}, e_PlayerRole_{player.role})\n"

        code_str += "\n"
        code_str += "\n"

    # addOponentPlayers:
    if len(opo_players ) >0:
        code_str += f"\tbuilder.SetTeam(Team.e_Right)\n"

        for player in opo_players:
            player_pos_sim = translator.pos_scenic_to_sim(player.position)
            #MIRRORING the position of the opponent player, as it seems the simulator mirrors it automatically
            code_str += f"\tbuilder.AddPlayer({-1*player_pos_sim.x}, {-1*player_pos_sim.y}, e_PlayerRole_{player.role})\n"

        code_str += "\n"
        code_str += "\n"

    return code_str