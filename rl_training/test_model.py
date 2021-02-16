import gfootball
import gym
import pygame
from gfootball.env import config, football_env
from stable_baselines3.common.evaluation import evaluate_policy

pygame.display.set_mode((1, 1), pygame.NOFRAME)
env = gfootball.env.create_environment("academy_empty_goal_close", number_of_left_players_agent_controls=1, render=True)

#env.render()



from stable_baselines3 import A2C

model = A2C.load("saved_model")

obs = env.reset()
pygame.display.set_mode((1, 1), pygame.NOFRAME)
for i in range(500):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)

    env.render()
    if done:
      obs = env.reset()