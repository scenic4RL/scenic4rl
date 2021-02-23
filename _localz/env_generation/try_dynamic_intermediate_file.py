import os
import random

import gfootball
import pygame




scenario = None
with open(f"dynamic.py", "r+") as f:
    scenario = f.read()

#print(scenario)

#pygame.display.set_mode((1, 1), pygame.NOFRAME)

"Dynamically writing on the same file doesn't work"
for i in range(1,5):

    with open("data","w+") as f:
        f.write(f"{i}\n{i+2}\n")

    path = gfootball.__path__[0]


    with open(f"{path}/scenarios/dynamic.py", "w+") as f:
        f.write(scenario)

    env = gfootball.env.create_environment("dynamic", number_of_left_players_agent_controls=1, render=False, representation="raw")

    #env.render()
    #pygame.display.set_mode((1, 1), pygame.NOFRAME)
    obs = env.reset()
    print(obs[0]["ball"])
    for _ in range(100):
        obs, reward, done, info = env.step([0])

        #print(reward)
        #env.render()
        if done:
          break