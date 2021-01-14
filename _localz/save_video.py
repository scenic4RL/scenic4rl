"""Script allowing to play the game by multiple players."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from gfootball.env.scenario_builder import Scenario
from gfootball.env import config
from gfootball.env import football_env

import gfootball_engine as libgame
from gfootball.env import football_action_set


settings = {
    'action_set': "full",
    'players': [f"agent:left_players=5,right_players=5"],
    'level': 'academy_corner',
    'dump_full_episodes': True,
    'dump_scores': True,
    'write_video': True,
    'tracesdir': 'dumps',
}

cfg = config.Config(settings)

env = football_env.FootballEnv(cfg)

env.render()
env.reset()
obs, _, done, _ = env.step([0] * 10)

step=0

while not done:
    obs, _, done, _ = env.step([football_action_set.action_shot] * 10)
    step+=1
    if step%20==0: print(f"{step} steps done")
    if done:
        print("Game ends")
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

