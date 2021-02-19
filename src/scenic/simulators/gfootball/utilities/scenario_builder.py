import gfootball
from scenic.simulators.gfootball.interface import get_scenario_python_str
from scenic.simulators.gfootball.utilities import translator
from scenic.simulators.gfootball.utilities.game_ds import GameDS
from scenic.syntax.veneer import verbosePrint


def get_level_name():
    pass

def initialize_gfootball_scenario(scene, gameds:GameDS):
    # set basic scenario attributes

    #scene_attrs = {}

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
    #scene_attrs.update(scene.params)

    module_path = gfootball.scenarios.__path__[0]

    param_names_for_gfootball_scenario_file = ["game_duration", "deterministic", "offsides", "end_episode_on_score",
                                          "end_episode_on_out_of_play", "end_episode_on_possession_change",
                                               "right_team_difficulty", "left_team_difficulty"]

    params_to_write = {k:v for k, v in scene.params.items() if k in param_names_for_gfootball_scenario_file}
    #params_to_write = scene.params

    out_file_name = module_path + "/" + scene.params["level"]+".py"
    verbosePrint(f"...Writing GFootBall Scenario to {out_file_name}")

    with open(out_file_name, "w+") as file:
        code_str = get_scenario_python_str(params_to_write, own_players=gameds.my_players, opo_players=gameds.op_players, ball=gameds.ball)
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



"""

def get_default_settings(player2="keyboard"):
    settings = {
        'action_set': "full",
        'dump_full_episodes': False,
        'real_time': True,
        'players': ['agent:left_players=1', f'{player2}:right_players=1'],
        # 'players': ['agent:left_players=1'],
        'level': GFOOTBALL_SCENARIO_FILENAME[:-3]
    }

    return settings
    
"""