import os
from random import choice
import gfootball
import pygame

files = ["z_test_0", "z_test_1"]
file_texts = []

for file in files:
    with open(f"{file}.py", "r+") as f:
        file_texts.append(f.read())

#for t in file_texts: print(t)

#pygame.display.set_mode((1, 1), pygame.NOFRAME)

"Dynamically writing on the same file doesn't work"
for _ in range(10):
    i = choice([0,1])
    scenario = file_texts[i]
    path = gfootball.__path__[0]

    rmpath = gfootball.__path__[0]+"/scenarios/__pycache__/dynamic.cpython-39.pyc"


    with open(f"{path}/scenarios/dynamic.py", "w+") as f:
        f.write(scenario)

    import importlib
    importlib.invalidate_caches()


    #if os.path.exists(rmpath): os.remove(rmpath)
    #del gfootball
    #if os.path.exists(rmpath): os.remove(rmpath)
    #import gfootball.scenarios.dynamic
    env = gfootball.env.create_environment("dynamic", number_of_left_players_agent_controls=1, render=False, representation="raw")

    #env.render()
    #pygame.display.set_mode((1, 1), pygame.NOFRAME)
    obs = env.reset()
    print(i, obs[0]["ball"])
    for _ in range(100):
        obs, reward, done, info = env.step([0])

        #print(reward)
        #env.render()
        if done:
          break