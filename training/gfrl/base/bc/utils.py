import argparse
import tempfile
import os.path as osp
import gym
import logging
from tqdm import tqdm
import tensorflow as tf


def generate_expert_successful_data(scenario_file, num_interactions=1000, file_name="expert_data", act_ndim=19):
	# from gfrl.base.run_my_ppo2 import create_single_scenic_environment
	import numpy as np
	expert_observations = []
	expert_actions = []
	expert_rewards = []

	gf_env_settings = {
		"stacked": True,
		"rewards": 'scoring',
		"representation": 'extracted',
		"players": [f"agent:left_players=1"],
		"action_set": "default",  # "default" "v2"
	}

	from scenic.simulators.gfootball.rl_interface import GFScenicEnv
	from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
	scenario = buildScenario(scenario_file)
	env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings, use_scenic_behavior_in_step=True,
					  constraints_checking=True)

	tr = 0

	obs_buf, acts_buf, rew_buf = [], [], []
	policy_rews = []

	with tqdm(total=num_interactions) as pbar:

		while (len(expert_observations) < num_interactions):

			if len(obs_buf) == 0:
				obs = env.reset()

			obs_buf.append(obs)
			obs, reward, done, info = env.step(env.action_space.sample())

			# rew_buf.append(reward)

			tr += reward
			# print(info)
			action = info["action_taken"]
			acts_buf.append(action)

			if done:

				# print(f"New Epi: {len(obs_buf)} R: {tr}")

				policy_rews.append(tr)

				if tr > 0:
					expert_observations.extend(obs_buf)
					expert_actions.extend(acts_buf)
					expert_rewards.append(tr)

					if len(expert_observations) > num_interactions:
						pbar.update(num_interactions)
					else:
						pbar.update(len(obs_buf))

					# print("Added new Api. Current Size: ", len(expert_observations))

				obs_buf, acts_buf, rew_buf = [], [], []
				obs = env.reset()
				tr = 0

	print("Collection Done")

	expert_observations = np.array(expert_observations)
	# expert_observations = np.moveaxis(expert_observations, [3], [1])
	acts = np.array(expert_actions)

	acts_oh = np.zeros((acts.shape[0], act_ndim))
	acts_oh[np.arange(acts.shape[0]), acts] = 1

	expert_rewards = np.array(expert_rewards)

	print("Expert observation shape: ", expert_observations.shape)
	print("Expert actions shape: ", acts_oh.shape)
	print("Num Expert Episode: ", expert_rewards.shape[0])
	print("Mean Expert Reward: ", expert_rewards.mean())

	print("Num Trajectories Collected: ", len(policy_rews))
	print("Mean Policy Reward: ", np.mean(policy_rews))
	print(f"Saved in: ", file_name)

	# np.savez(expert_file_name, obs=mb_obs, acs=mb_act_oh, num_epi = num_episodes, mean_reward = np.sum(mb_rewards)/num_episodes)
	np.savez_compressed(
		file_name,
		acs=acts_oh,
		obs=expert_observations,
		num_epi=expert_rewards.shape[0],
		mean_reward=expert_rewards.mean(),
		rewards=expert_rewards,
		policy_mean_reward=np.mean(policy_rews),
		policy_total_trajectories=len(policy_rews)
	)
	return expert_observations, acts_oh, expert_rewards


"""
def generate_dataset(scenario, num_interactions, save_file_path):
	
	pass
"""