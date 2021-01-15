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
    'level': '5_vs_5',
}

cfg = config.Config(settings)

env = football_env.FootballEnv(cfg)

env.render()
env.reset()
obs, _, done, _ = env.step([0] * 10)


while True:
    obs, _, done, _ = env.step([football_action_set.action_shot] * 10)
    print("step")
    if done:
        break

print("Game ends")