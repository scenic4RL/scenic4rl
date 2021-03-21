import gfootball
from scenic.simulators.gfootball.interface import get_scenario_python_str
from scenic.simulators.gfootball.utilities import translator
from scenic.simulators.gfootball.utilities.game_ds import GameDS
from scenic.syntax.veneer import verbosePrint
import os
import numpy as np

SCENARIO_SUBFOLDER_NAME = 'scenic_exp'

def get_level_name(path, scene):
    import uuid
    #new_index = len(os.listdir(f"{path}/{SCENARIO_SUBFOLDER_NAME}/"))
    #return f"{scene.name}"
    return "dynamic"

    #return f"{uuid.uuid4()}_{scene.name}"

class SceneInfo():

    def __init__(self, params, ball, my_players, op_players):

        """
        :param params:      dictionary of parameters
        :param ball:        tuple position x, y
        :param my_players:  list of (x,y,role)
        :param op_players:  list of (x,y,role)
        """

        self.params = params
        self.ball = ball
        self.my_players = my_players
        self.op_players = op_players

    def __str__(self):
        return str(self.ball)  + str (self.my_players)



def initialize_gfootball_scenario(scene, gameds:GameDS):
    import scenic

    #data_path = scenic.__path__[0]
    #data paths and other variable



    module_path = gfootball.scenarios.__path__[0]
    level_name = get_level_name(module_path, scene)

    out_file_name = f"{module_path}/{level_name}.py"


    data_file_dir = scenic.__path__[0] + f"/simulators/gfootball/scene_data"
    import os 
    os.makedirs(data_file_dir, exist_ok=True)
    data_file_path = f"{data_file_dir}/{level_name}"
    


    #1. Write file in gf/scenarios folder

    #   copy template file: template_gf_scenario.py
    #   later: change data file location dynamically
    #   (later - only write if it doesnt exist)

    verbosePrint(f"...Writing GFootBall Scenario to {out_file_name}")

    with open(out_file_name, "w+") as gout:

        tmplt_path = scenic.__path__[0]+"/simulators/gfootball/utilities/template_gf_scenario.py"
        with open(tmplt_path, "r+") as gin:
            code_str = gin.read()
            """Prepend Data File Path"""
            pre = f"data_path = '{data_file_path}'\n"
            code_str = pre+code_str
            #verbosePrint(code_str)
            #print(code_str)
            gout.write(code_str)

    #2. Write data in data file
    #   -> create a folder in a platform-independent way
    #


    #prepare the SceneInfo object
    param_names_for_gfootball_scenario_file = ["game_duration", "deterministic", "offsides", "end_episode_on_score",
                                          "end_episode_on_out_of_play", "end_episode_on_possession_change",
                                               "right_team_difficulty", "left_team_difficulty"]

    params_to_write = {k:v for k, v in scene.params.items() if k in param_names_for_gfootball_scenario_file}
    ball_sim = translator.pos_scenic_to_sim(gameds.ball.position)
    ball = (ball_sim.x, ball_sim.y)

    #generate player tuples
    own_player_tuples = []
    op_player_tuples = []

    import gfootball_engine as libgame
    role_map = {"GK": libgame.e_PlayerRole.e_PlayerRole_GK,
                "CB": libgame.e_PlayerRole.e_PlayerRole_CB,
                "LB": libgame.e_PlayerRole.e_PlayerRole_LB,
                "RB": libgame.e_PlayerRole.e_PlayerRole_RB,
                "DM": libgame.e_PlayerRole.e_PlayerRole_DM,
                "CM": libgame.e_PlayerRole.e_PlayerRole_CM,
                "LM": libgame.e_PlayerRole.e_PlayerRole_LM,
                "RM": libgame.e_PlayerRole.e_PlayerRole_RM,
                "AM": libgame.e_PlayerRole.e_PlayerRole_AM,
                "CF": libgame.e_PlayerRole.e_PlayerRole_CF,
                "CMM": libgame.e_PlayerRole.e_PlayerRole_CM,
                "CML": libgame.e_PlayerRole.e_PlayerRole_CM,
                "CMR": libgame.e_PlayerRole.e_PlayerRole_CM,}

    for players, player_tuple_array, mirror in zip([gameds.my_players, gameds.op_players],
                                           [own_player_tuples, op_player_tuples],
                                           [False, True]):
        if len(players) > 0:
            from scenic.simulators.gfootball.utilities.constants import RoleCode

            for player in players:
                player_pos_sim = translator.pos_scenic_to_sim(player.position, mirrorx=mirror, mirrory=mirror)
                player_tup = (player_pos_sim.x, player_pos_sim.y, role_map[player.role])
                player_tuple_array.append(player_tup)

            player_tuple_array.sort(key=lambda x: 0 if x[2] == 'e_PlayerRole_GK' else 1)

    scene_info = SceneInfo(params=params_to_write, ball=ball, my_players=own_player_tuples, op_players=op_player_tuples)
    #print(scene_info)
    import pickle
    pickle.dump(scene_info, open(data_file_path, "wb"))

    return f"{level_name}"

    #return f"{SCENARIO_SUBFOLDER_NAME}.{level_name}"


def initialize_gfootball_scenario_v0(scene, gameds: GameDS):
    # set basic scenario attributes

    # scene_attrs = {}

    """
    default_scene_params = {
        'game_duration': 400,
        'deterministic': False,
        'offsides': False,
        'end_episode_on_score': True,
        'end_episode_on_out_of_play': False,
        'end_episode_on_possession_change': False,
        'right_team_difficulty': 0.0,    ??
        'left_team_difficulty': 0.0      ??
    }

    # Set default parameters for scene
    scene_attrs.update(default_scene_params)
    """
    # UPDATE SCENE PARAMETERS
    # scene_attrs.update(scene.params)

    module_path = gfootball.scenarios.__path__[0]

    param_names_for_gfootball_scenario_file = ["game_duration", "deterministic", "offsides", "end_episode_on_score",
                                               "end_episode_on_out_of_play", "end_episode_on_possession_change",
                                               "right_team_difficulty", "left_team_difficulty"]

    params_to_write = {k: v for k, v in scene.params.items() if k in param_names_for_gfootball_scenario_file}
    # params_to_write = scene.params

    level_name = get_level_name(module_path, scene)
    # out_file_name = module_path + "/" + scene.params["level"]+ ".py"
    # out_file_name = f"{module_path}/{SCENARIO_SUBFOLDER_NAME}/{level_name}.py"
    out_file_name = f"{module_path}/{level_name}.py"

    verbosePrint(f"...Writing GFootBall Scenario to {out_file_name}")

    with open(out_file_name, "w+") as file:
        code_str = get_scenario_python_str(params_to_write, own_players=gameds.my_players,
                                           opo_players=gameds.op_players, ball=gameds.ball)
        verbosePrint(code_str)
        file.write(code_str)

    """
    print("scene id:", id(scene))
    with open(module_path + "/" + scene.params["level"] + ".py", "r+") as file:
        txt = file.read()
        print("Scenario File: ")
        print(txt)
        print("##"*80)
    """
    return f"{level_name}"