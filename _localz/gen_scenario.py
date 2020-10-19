"""Script allowing to play the game by multiple players."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from gfootball.env.scenario_builder import Scenario
from gfootball.env import config
from gfootball.env import football_env

import gfootball_engine as libgame
import gfootball
Player = libgame.FormationEntry
Role = libgame.e_PlayerRole
Team = libgame.e_Team
#AddPlayer(self, x, y, role, lazy=False, controllable=True):


import gfootball


#build a scenario file from arguments
def build_scenario_file(scene_attrs):
    code_str = ""
    code_str += "from . import *\n"

    code_str += "def build_scenario(builder):\n"

    #basic settings:
    for name, value in scene_attrs.items():
        code_str += f"\t{name} = {value}\n"

    code_str += "\n"
    code_str += "\n"

    return code_str

#set basic scenario attributes
scene_attrs = {}

scene_attrs['game_duration'] = 400
scene_attrs['deterministic'] = False
scene_attrs['offsides'] = False
scene_attrs['end_episode_on_score'] = True
scene_attrs['end_episode_on_out_of_play'] = False
scene_attrs['end_episode_on_possession_change'] = False


#write scenario to file
module_path = gfootball.scenarios.__path__[0]
print(module_path)
file_name = "dynamic.py"


with open(module_path+"/"+file_name, "w+") as file:
    code_str = build_scenario_file(scene_attrs)
    print(code_str)
    file.write(code_str)


settings = {
    'action_set': "full",
    'dump_full_episodes': False,
    'real_time': True,
    'players': ['keyboard:left_players=1'],
    'level': file_name[:-3]
}
cfg = config.Config(settings)


env = football_env.FootballEnv(cfg)


env.render()
env.step([])
env.reset()


while True:
    _, _, done, _ = env.step([])
    if done:
        env.reset()



