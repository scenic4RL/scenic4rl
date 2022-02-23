from random import randint

import gfootball
import gym
# from scenic.simulators.gfootball.rl import pfrl_training

from gfootball.env import football_action_set
from tqdm import tqdm

# Curriculum Learning usinf rllib: https://docs.ray.io/en/latest/rllib-training.html#curriculum-learning
from scenic.simulators.gfootball.utilities import scenic_helper
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

"""Multi agent environment with scenic behaviors, modified from v2.
Will mimic vanilla GRF multi-agent env returns
Select n closest players to ball to control. (num_left_controlled)
TODO: scale obs dim option
Always does pre_step (hence, computes all actions in scenic), and post_step"""
class GFScenicEnv_v3(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self, initial_scenario, num_left_controlled, gf_env_settings=None, allow_render = False, rank=0):
		super(GFScenicEnv_v3, self).__init__()

		if gf_env_settings is None:
			gf_env_settings = {}
		self.gf_env_settings = gf_env_settings
		self.allow_render = allow_render
		self.scenario = initial_scenario
		self.rank = rank

		# TODO: custom channel dimension support
		# bug: the following code only change obs space dim, not actual obs dim
		# self.channel_dimensions = (72, 96)
		# if "channel_dimensions" in gf_env_settings:
		# 	self.channel_dimensions = gf_env_settings["channel_dimensions"]
		# 	assert len(self.channel_dimensions) == 2, "Provide valid dim in (h, w)"
		# 	print(f"Use custom channel_dimensions of {self.channel_dimensions}")
		assert "channel_dimensions" not in gf_env_settings, "Custom Dim not supported."
		self.channel_dimensions = (72, 96)

		# determine player to control
		# TODO: Validate n closest players to ball to control. (num_left_controlled)
		assert num_left_controlled > 1, "Use GFScenicEnv_v2, not v3, for single agent"
		self.num_left_controlled = num_left_controlled

		from gym.spaces.multi_discrete import MultiDiscrete
		from gym.spaces import Box, Tuple
		from numpy import uint8

		#assert self.gf_env_settings["action_set"] == "default" or use_scenic_behavior_in_step
		assert self.gf_env_settings["representation"] == "extracted"
		assert self.gf_env_settings["stacked"] == True

		# multiagent obs is a list of player's respective obs
		# self.observation_space = Tuple([Box(low=0, high=255, shape=(72, 96, 16), dtype=uint8)] * self.num_left_controlled)
		self.observation_space = Box(low=0, high=255, shape=(self.num_left_controlled, self.channel_dimensions[0], self.channel_dimensions[1], 16), dtype=uint8)
		# print("Obs Space: ", self.observation_space)
		self.action_space = MultiDiscrete([19] * self.num_left_controlled)
		# print("Act Space: ", self.action_space)



	def reset(self):
		for _ in range(100):
			try:
				self.scene, _ = scenic_helper.generateScene(self.scenario)
				if self.scene is None:
					return None

				if hasattr(self, "simulation"): self.simulation.get_underlying_gym_env().close()

				from scenic.simulators.gfootball.simulator import GFootBallSimulation
				# notice we should use v2 simulation env type for controlling multiple players
				self.simulation = GFootBallSimulation(scene=self.scene, settings={}, for_gym_env=True,
													  render=self.allow_render, verbosity=1,
													  env_type="v2",
													  gf_env_settings=self.gf_env_settings,
													  tag=str(self.rank),
													  num_left_controlled=self.num_left_controlled)

				self.gf_gym_env = self.simulation.get_underlying_gym_env()

				obs = self.simulation.reset()
				player_idx = self.simulation.get_controlled_player_idx()

				self.simulation.pre_step()

				# note this only works if obs is ndarray
				return obs[player_idx]

			except Exception as e:
				print("Resample Script. Cause Error: ", e)
				pass


	def step(self, provided_actions):
		# Execute one time step within the environment

		assert len(provided_actions) == self.num_left_controlled, f"Action dim mismatch. Got {len(provided_actions)}, expect {self.num_left_controlled}."
		assert 19 not in provided_actions, f"Cannot take built in ai action for rl! act: {provided_actions}"

		#self.simulation.pre_step()

		scenic_actions = self.simulation.get_actions()
		player_idx = self.simulation.get_controlled_player_idx() # this is a list


		actions = scenic_actions.copy()
		# apply rl inputs
		# actions[player_idx] = provided_actions
		for i, p_idx in enumerate(player_idx):
			actions[p_idx] = provided_actions[i]

		obs, rew, done, info = self.simulation.step(actions)

		self.simulation.post_step()
		if not done:
			self.simulation.pre_step() # For computing the actions before step is called

		return obs[player_idx], rew[player_idx], done, info

	def render(self, mode='human', close=False):
		# Render the environment to the screen
		# For weird pygame rendering issue on Mac, rendering must be called in utilities/env_creator/create_environment
		return None


def test_obs():
	gf_env_settings = {
		"stacked": True,
		"rewards": 'scoring',
		"representation": 'extracted',
		"real_time": True,
		# "channel_dimensions": (42, 42)
		"dump_full_episodes": True,
		"dump_scores": True,
		"tracesdir": "/home/mark/workplace/gf/scenic4rl/replays",
		"write_video": True,
	}

	from scenic.simulators.gfootball.rl.gfScenicEnv_v3 import GFScenicEnv_v3

	num_trials = 1
	num_left_to_be_controlled = 2
	scenario_file = "/home/mark/workplace/gf/scenic4rl/training/gfrl/_scenarios/grf/run_pass_shoot.scenic"
	scenario = buildScenario(scenario_file)

	env = GFScenicEnv_v3(initial_scenario=scenario, num_left_controlled=num_left_to_be_controlled, gf_env_settings=gf_env_settings, allow_render=True)

	# from scenic.simulators.gfootball.rl import utils

	num_epi = 0
	total_r = 0

	for i in tqdm(range(0, num_trials)):
		obs = env.reset()
		assert obs.shape == (num_left_to_be_controlled,72,96,16), obs.shape
		done = False
		# input("Enter")
		while not done:
			action = env.action_space.sample()
			action = [1,3] # 1 left 3 top 5 right 7 down
			obs, reward, done, info = env.step(action)
			assert obs.shape == (num_left_to_be_controlled,72,96,16), obs.shape
			total_r += reward
			if done:
				obs = env.reset()
				num_epi += 1

	perf =  total_r / num_epi
	print("random agent performance: ", perf)


if __name__ == '__main__':
	test_obs()
