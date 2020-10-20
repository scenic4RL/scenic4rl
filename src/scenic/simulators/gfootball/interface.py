from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from gfootball.env.scenario_builder import Scenario
from gfootball.env import config
from gfootball.env import football_env

import gfootball_engine as libgame

Player = libgame.FormationEntry
Role = libgame.e_PlayerRole
Team = libgame.e_Team
#AddPlayer(self, x, y, role, lazy=False, controllable=True):


import gfootball


#build a scenario file from arguments
def get_scenario_python_str(scene_attrs, own_players, opo_players):
    code_str = ""
    code_str += "from . import *\n"

    code_str += "def build_scenario(builder):\n"

    #basic settings:
    for name, value in scene_attrs.items():
        code_str += f"\t{name} = {value}\n"

    #addOwnPlayers:


    code_str += "\n"
    code_str += "\n"

    return code_str



#my players


#write scenario to file

GFOOTBALL_SCENARIO_FILENAME = "dynamic.py"





def initialize_gfootball_scenario():

    # set basic scenario attributes
    scene_attrs = {}

    scene_attrs['game_duration'] = 400
    scene_attrs['deterministic'] = False
    scene_attrs['offsides'] = False
    scene_attrs['end_episode_on_score'] = True
    scene_attrs['end_episode_on_out_of_play'] = False
    scene_attrs['end_episode_on_possession_change'] = False

    module_path = gfootball.scenarios.__path__[0]

    with open(module_path + "/" + GFOOTBALL_SCENARIO_FILENAME, "w+") as file:
        code_str = get_scenario_python_str(scene_attrs)
        print(code_str)
        file.write(code_str)

def build_config():
    settings = {
        'action_set': "full",
        'dump_full_episodes': False,
        'real_time': True,
        'players': ['keyboard:left_players=1'],
        'level': GFOOTBALL_SCENARIO_FILENAME[:-3]
    }

    cfg = config.Config(settings)
    pass


