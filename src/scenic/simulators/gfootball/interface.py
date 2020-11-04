from scenic.simulators.gfootball.utilities import translator
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
            pos = translator.pos_sim_to_scenic(obs[tp][ind])
            direction = obs[f"{tp}_direction"][ind]
            tired = obs[f"{tp}_tired_factor"][ind]

            player_info[role] = {}
            player_info[role]['pos'] = pos
            player_info[role]['direction'] = direction
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
            obj.tired = my_player_info[role]["tired"]
            obj.active = my_player_info[role]["active"]
            obj.ball_owned = my_player_info[role]["ball_owned"]


        elif "OpPlayer" in str(type(obj)):
            role = obj.role
            obj.position = op_player_info[role]["pos"]
            obj.tired = op_player_info[role]["tired"]

        elif "Ball" in str(type(obj)):
            obj.position = translator.pos_sim_to_scenic(obs['ball'])
            obj.direction = obs["ball_direction"]
            obj.owned_team = obs['ball_owned_team']
            obj.owned_player = obs['ball_owned_player']