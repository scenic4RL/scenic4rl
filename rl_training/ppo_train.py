import gfootball
import gym
import pygame
from gfootball.env import config, football_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.policies import ActorCriticCnnPolicy
import os

# Create save dir
from rl_training.gfootball_impala_cnn import Custom_Basic_CNN

ALGO = PPO
n_eval_episodes = 10
total_training_timesteps = 5000
save_dir = "./saved_models"
logdir = "./tboard"

os.makedirs(save_dir, exist_ok=True)
os.makedirs(logdir, exist_ok=True)


#academy_empty_goal_close, academy_run_pass_and_shoot_with_keeper
# rewards='scoring,checkpoints'
env = gfootball.env.create_environment("academy_corner", stacked=True, rewards='scoring, checkpoints', number_of_left_players_agent_controls=1, render=False)
#env.observation_space: Box(0, 255, (72, 96, 16), uint8), Action space: Discrete(19)
env = Monitor(env)

#model = ALGO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)
model = ALGO("CnnPolicy", env, verbose=1, tensorboard_log=logdir)
model.learn(total_timesteps=total_training_timesteps, tb_log_name="final")

model.save(f"{save_dir}/PPO_basic_{total_training_timesteps}")

mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=n_eval_episodes)
print(f"Eval Mean Rewards: {mean_reward:0.4f} Episodes: {n_eval_episodes}")