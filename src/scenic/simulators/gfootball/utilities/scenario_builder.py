import gfootball
from scenic.simulators.gfootball.interface import get_scenario_python_str
from scenic.simulators.gfootball.utilities import translator
from scenic.simulators.gfootball.utilities.game_ds import GameDS


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
        'right_team_difficulty': 0.0,
        'left_team_difficulty': 0.0
    }
    
    # Set default parameters for scene
    scene_attrs.update(default_scene_params)
    """
    # UPDATE SCENE PARAMETERS
    #scene_attrs.update(scene.params)

    module_path = gfootball.scenarios.__path__[0]

    """
    from scenic.simulators.gfootball.model import Player, Ball
    ball = None
    my_players = []
    op_players = []

    from scenic.simulators.gfootball.interface import is_player, is_my_player, is_op_player, is_ball
    for obj in objects:
        #print(obj, type(obj))

        # change with isinstance
        if is_my_player(obj):
            my_players.append(obj)

        elif is_op_player(obj):
            op_players.append(obj)

        elif is_ball(obj):
            # print(f"Ball {dir(obj)}")
            ball = obj
    """

    print(f"...Writing GFootBall Scenario to {module_path}")

    with open(module_path + "/" + scene.params["level"]+".py", "w+") as file:
        code_str = get_scenario_python_str(scene.params, own_players=gameds.my_players, opo_players=gameds.op_players, ball=gameds.ball)
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