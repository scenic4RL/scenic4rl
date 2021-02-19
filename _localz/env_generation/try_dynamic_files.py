from pprint import pprint
from random import choice

import gfootball
import gfootball
import gym
import pygame
from gfootball.env import config, football_env
path = gfootball.__path__[0]
files = ["z_test_0", "z_test_1"]

file_texts = []

for file in files:
    with open(f"{path}/scenarios/{file}.py", "r+") as f:
        file_texts.append(f.read())

#for t in file_texts:print(t)
#pprint(file_texts)
pygame.display.set_mode((1, 1), pygame.NOFRAME)

"Dynamically writing on the same file doesnt work"
for _ in range(10):
    #level = choice(files)
    #print(level)
    lv = choice(file_texts)

    with open(f"{path}/scenarios/dynamic.py", "w+") as f:
        f.write(lv)

    env = gfootball.env.create_environment("dynamic", number_of_left_players_agent_controls=1, render=False, representation="raw")

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