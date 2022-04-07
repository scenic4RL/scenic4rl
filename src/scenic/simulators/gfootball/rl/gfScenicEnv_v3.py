from random import randint

import gfootball
import gym
# from scenic.simulators.gfootball.rl import pfrl_training

from gfootball.env import football_action_set
from tqdm import tqdm

# Curriculum Learning usinf rllib: https://docs.ray.io/en/latest/rllib-training.html#curriculum-learning
from scenic.simulators.gfootball.utilities import scenic_helper
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

from gym.spaces.multi_discrete import MultiDiscrete
from gym.spaces import Box, Tuple
from numpy import uint8

"""Multi agent environment with scenic behaviors, modified from v2.
Will mimic vanilla GRF multi-agent env returns.
player_control_mode:
	EITHER dynamically control players closest to the ball: input number of players controlled
	OR fixed player control: input "all" or "allNonGK"
Select n closest players to ball to control. (num_left_controlled)
TODO: scale obs dim option
Always does pre_step (hence, computes all actions in scenic), and post_step"""
class GFScenicEnv_v3(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self, initial_scenario, player_control_mode, gf_env_settings=None, allow_render = False, rank=0):
		super(GFScenicEnv_v3, self).__init__()

		if gf_env_settings is None:
			gf_env_settings = {}
		self.gf_env_settings = gf_env_settings
		# will update render option after initial reset
		self.allow_render = False
		self.scenario = initial_scenario
		self.rank = rank

		# custom channel dimension not supported
		# issue: the following code only change obs space dim, not actual obs dim
		# self.channel_dimensions = (72, 96)
		# if "channel_dimensions" in gf_env_settings:
		# 	self.channel_dimensions = gf_env_settings["channel_dimensions"]
		# 	assert len(self.channel_dimensions) == 2, "Provide valid dim in (h, w)"
		# 	print(f"Use custom channel_dimensions of {self.channel_dimensions}")
		assert "channel_dimensions" not in gf_env_settings, "Custom Dim not supported."
		self.channel_dimensions = (72, 96)

		# determine player to control

		# Validate n closest players to ball to control. (player_control_mode)
		player_control_mode = str(player_control_mode)
		assert player_control_mode.isnumeric() or player_control_mode in ("all", "allNonGK", "2closest", "3closest")
		if player_control_mode.isnumeric() and int(player_control_mode) <= 1:
			raise ValueError("Use GFScenicEnv_v2, not v3, for single agent")
		self.player_control_mode = player_control_mode


		#assert self.gf_env_settings["action_set"] == "default" or use_scenic_behavior_in_step
		assert self.gf_env_settings["representation"] == "extracted"
		assert self.gf_env_settings["stacked"] == True

		# do reset once to determine number of players controlled
		self.reset()
		self.allow_render = allow_render
		self.num_left_controlled = self.simulation.num_left_controlled
		assert not (self.player_control_mode == "allNonGK" and self.num_left_controlled <= 1), "Scenario only has GK."

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
													  player_control_mode=self.player_control_mode)

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
		player_idx = self.simulation.get_controlled_player_idx()  # this is a list


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
		# "channel_dimensions": (42, 42)
		"dump_full_episodes": True,
		"dump_scores": True,
		"tracesdir": "/home/mark/workplace/gf/scenic4rl/replays",
		"write_video": True,
	}

	# from scenic.simulators.gfootball.rl.gfScenicEnv_v3 import GFScenicEnv_v3

	num_trials = 3
	num_left_to_be_controlled = 2
	scenario_file = "/home/mark/workplace/gf/scenic4rl/training/gfrl/_scenarios/grf/run_pass_shoot.scenic"
	scenario = buildScenario(scenario_file)

	env = GFScenicEnv_v3(initial_scenario=scenario, player_control_mode="allNonGK", gf_env_settings=gf_env_settings, allow_render=True)

	num_epi = 0
	total_r = 0

	for i in tqdm(range(0, num_trials)):
		obs = env.reset()
		assert obs.shape == (num_left_to_be_controlled,72,96,16), obs.shape
		done = False
		# input("Enter")
		while not done:
			action = env.action_space.sample()
			action = [5, 1] # 1 left 3 top 5 right 7 down
			obs, reward, done, info = env.step(action)
			assert obs.shape == (num_left_to_be_controlled,72,96,16), obs.shape
			total_r += reward

		num_epi += 1

	perf =  total_r / num_epi
	print("random agent performance: ", perf)


if __name__ == '__main__':
	test_obs()
