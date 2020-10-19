"""Script allowing to play the game by multiple players."""

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
settings = {
    'action_set': "full",
    'dump_full_episodes': False,
    'real_time': True,
    'players': ['keyboard:left_players=1'],
    'level': 'academy_empty_goal'


}
init_cfg = config.Config(settings)
scenario = Scenario(init_cfg)

scenario.SetBallPosition(0.5,0)

scenario.SetTeam(Team.e_Left)
scenario.AddPlayer(0.0, 0.1, libgame.e_PlayerRole.e_PlayerRole_CF)
scenario.AddPlayer(0.0, -0.1, libgame.e_PlayerRole.e_PlayerRole_RM)

built_cfg = scenario._config
env = football_env.FootballEnv(built_cfg)


env.render()
env.step([])
env.reset()


while True:
    _, _, done, _ = env.step([])
    if done:
        env.reset()

"""
try:
    while True:
        _, _, done, _ = env.step([])
        if done:
            env.reset()
except KeyboardInterrupt:
    logging.warning('Game stopped, writing dump...')
    env.write_dump('shutdown')
    exit(1)
    
"""

