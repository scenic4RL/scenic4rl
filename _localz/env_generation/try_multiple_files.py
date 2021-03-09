from random import choice
import gfootball
import gym
import pygame
from gfootball.env import config, football_env


path = gfootball.__file__
"If Using a directory other then scenario itself, copy the .__init__ file into that folder"
files = ["scenic_exp.z_test_0", "scenic_exp.z_test_1"]


pygame.display.set_mode((1, 1), pygame.NOFRAME)


for _ in range(10):
    level = choice(files)
    #print(level)
    env = gfootball.env.create_environment(level, number_of_left_players_agent_controls=1, render=False, representation="raw")

    #env.render()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    obs = env.reset()
    print(obs[0]["ball"])
    for _ in range(100):
        obs, reward, done, info = env.step([0])

        #print(reward)
        #env.render()
        if done:
          break