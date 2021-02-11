import gfootball
import gym
import pygame
from gfootball.env import config, football_env

pygame.display.set_mode((1, 1), pygame.NOFRAME)
env = gfootball.env.create_environment("academy_empty_goal_close", number_of_left_players_agent_controls=1, render=True)

env.render()
pygame.display.set_mode((1, 1), pygame.NOFRAME)
obs = env.reset()

for i in range(100):
    obs, reward, done, info = env.step([0])
    print(reward)
    env.render()
    if done:
      break