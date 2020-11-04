import gfootball
from scenic.simulators.gfootball.interface import get_scenario_python_str
from scenic.simulators.gfootball.utilities import translator


GFOOTBALL_SCENARIO_FILENAME = "dynamic.py"


def initialize_gfootball_scenario(scene, objects):
    # set basic scenario attributes

    scene_attrs = {}

    default_scene_params = {
        'game_duration': 400,
        'deterministic': False,
        'offsides': False,
        'end_episode_on_score': True,
        'end_episode_on_out_of_play': False,
        'end_episode_on_possession_change': False,
        'right_team_difficulty': 0.0,
        'left_team_difficulty': 0.0
    }

    # Set default parameters for scene
    scene_attrs.update(default_scene_params)

    # UPDATE SCENE PARAMETERS
    scene_attrs.update(scene.params)

    module_path = gfootball.scenarios.__path__[0]

    from scenic.simulators.gfootball.model import Player, Ball
    ball = None
    my_players = []
    op_players = []
    for obj in objects:
        print(obj, type(obj))

        # change with isinstance
        if "MyPlayer" in str(type(obj)):
            my_players.append(obj)

        elif "OpPlayer" in str(type(obj)):
            op_players.append(obj)

        elif "Ball" in str(type(obj)):
            # print(f"Ball {dir(obj)}")
            ball = obj

    print(f"...Writing GFootBall Scenario to {module_path}")

    with open(module_path + "/" + GFOOTBALL_SCENARIO_FILENAME, "w+") as file:
        code_str = get_scenario_python_str(scene_attrs, own_players=my_players, opo_players=op_players, ball=ball)
        print(code_str)
        file.write(code_str)



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