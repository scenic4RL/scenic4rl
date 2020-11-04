import gfootball
from scenic.simulators.gfootball.utilities import translator


GFOOTBALL_SCENARIO_FILENAME = "dynamic.py"


def get_scenario_python_str(scene_attrs, own_players, opo_players, ball):
    code_str = ""
    code_str += "from . import *\n"

    code_str += "def build_scenario(builder):\n"

    # basic settings:
    for name, value in scene_attrs.items():
        code_str += f"\tbuilder.config().{name} = {value}\n"

    # add Ball
    ball_pos_sim = translator.pos_scenic_to_sim(ball.position)
    code_str += f"\tbuilder.SetBallPosition({ball_pos_sim.x}, {ball_pos_sim.y})\n"

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
            code_str += f"\tbuilder.AddPlayer({player_pos_sim.x}, {player_pos_sim.y}, e_PlayerRole_{player.role})\n"

        code_str += "\n"
        code_str += "\n"

    return code_str


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