from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pygame
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
pygame.display.set_mode((1, 1), pygame.NOFRAME)
env = football_env.FootballEnv(cfg)

env.render()
pygame.display.set_mode((1, 1), pygame.NOFRAME)
env.reset()
obs, _, done, _ = env.step([0] * 10)


while True:
    obs, _, done, _ = env.step([football_action_set.action_shot] * 10)
    print("step")
    if done:
        break

print("Game ends")