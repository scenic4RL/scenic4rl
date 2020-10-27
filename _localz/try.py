"""Script allowing to play the game by multiple players."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from gfootball.env.scenario_builder import Scenario
from gfootball.env import config
from gfootball.env import football_env

import gfootball_engine as libgame
from gfootball.env import football_action_set

#AddPlayer(self, x, y, role, lazy=False, controllable=True):
settings = {
    'action_set': "full",
    'dump_full_episodes': True,
    'real_time': False,
    'players': ["agent:left_players=1", "bot:right_players=1"],
    'level': '1_vs_1_easy'
}
#    'tracesdir': '~/gfootball-dumps/',
#    'write_video': True

cfg = config.Config(settings)


env = football_env.FootballEnv(cfg)


env.render()
env.step([0])
env.reset()


while True:
    _, _, done, _ = env.step([football_action_set.action_shot])
    #_, _, done, _ = env.step([])
    if done:
        break

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

