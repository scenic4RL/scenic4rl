import gfootball
import gym
import pygame
from gfootball.env import config, football_env

#academy_run_to_score_with_keeper
#academy_empty_goal_close
#academy_run_pass_and_shoot_with_keeper
#academy_counterattack_easy
#academy_counterattack_hard
pygame.display.set_mode((1, 1), pygame.NOFRAME)
env = gfootball.env.create_environment("academy_run_pass_and_shoot_with_keeper", number_of_left_players_agent_controls=1, render=True,
                                       other_config_options={"real_time":True, "action_set": "v2"})

env.render()
pygame.display.set_mode((1, 1), pygame.NOFRAME)
obs = env.reset()
input("Enter any key to run")
while True:

    obs, reward, done, info = env.step([19])
    print(reward)
    env.render()
    if done:
      break