from scenic.simulators.gfootball import rl_interface
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
from stable_baselines3 import PPO
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
import gym
from tqdm import tqdm
import numpy as np
import torch as th
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from stable_baselines3 import PPO, A2C, SAC, TD3
from stable_baselines3.common.evaluation import evaluate_policy

from torch.utils.data.dataset import Dataset, random_split
import os

def mean_reward(env, num_trials=1):

    obs = env.reset()
    #env.render()
    num_epi = 0
    total_r = 0
    from tqdm import tqdm
    for i in tqdm(range(0, num_trials)):

        done = False

        while not done:
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            #env.render()
            total_r+=reward
            if done:
                obs = env.reset()
                num_epi +=1

    return total_r/num_epi


def generate_expert_data(env, num_interactions=1000, file_name="expert_data"):
    expert_observations = []
    expert_actions = []

    obs = env.reset()

    for i in tqdm(range(num_interactions)):
        expert_observations.append(obs)

        obs, reward, done, info = env.step(env.action_space.sample())
        # print(info)
        action = info["action_taken"]
        expert_actions.append(action)

        if done:
            obs = env.reset()

    expert_observations = np.array(expert_observations)
    expert_observations = np.moveaxis(expert_observations, [3], [1])
    expert_actions = np.array(expert_actions)
    print("Expert observation shape: ", expert_observations.shape)
    print("Expert actions shape: ", expert_actions.shape)

    np.savez_compressed(
        file_name,
        expert_actions=expert_actions,
        expert_observations=expert_observations,
    )
    return expert_observations, expert_actions



#generate expert data

gf_env_settings = {
    "stacked": True,
    "rewards": 'scoring',
    "representation": 'extracted',
    "players": [f"agent:left_players=1"],
    "real_time": False,
    "action_set": "default",#"default" "v2"
}

cwd = os.getcwd()
datagen_scenario_file = f"{cwd}/run_to_score_with_behave.scenic"
datagen_scenario = buildScenario(datagen_scenario_file)

num_interactions = 50000
file_name = f"expert_data_{num_interactions}"
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

datagen_env = GFScenicEnv(initial_scenario=datagen_scenario, gf_env_settings=gf_env_settings, use_scenic_behavior_in_step=True)
print("Mean Reward of Scenic Behavior Agent", mean_reward(datagen_env, num_trials=20))



expert_observations, expert_actions = generate_expert_data(datagen_env, num_interactions=num_interactions, file_name=file_name)

loaded_data = np.load(f"{file_name}.npz")
expert_observations = loaded_data["expert_observations"]
expert_actions = loaded_data["expert_actions"]
print(f"Loaded data obs: {expert_observations.shape}, actions: {expert_actions.shape}")

