from random import randint

import gfootball
import gym
# from scenic.simulators.gfootball.rl import pfrl_training

from gfootball.env import football_action_set

# Curriculum Learning usinf rllib: https://docs.ray.io/en/latest/rllib-training.html#curriculum-learning
from scenic.simulators.gfootball.utilities import scenic_helper
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario


class GFScenicEnv_v2(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self, initial_scenario, gf_env_settings={}, allow_render = False, rank=0):
		super(GFScenicEnv_v2, self).__init__()

		self.gf_env_settings = gf_env_settings
		self.allow_render = allow_render
		self.scenario = initial_scenario
		self.rank = rank

		from gym.spaces.discrete import Discrete
		from gym.spaces import Box
		from numpy import uint8

		#assert self.gf_env_settings["action_set"] == "default" or use_scenic_behavior_in_step
		assert self.gf_env_settings["representation"] == "extracted"
		assert self.gf_env_settings["stacked"] == True

		self.observation_space = Box(low=0, high=255, shape=(72, 96, 16), dtype=uint8)
		self.action_space = Discrete(19)



	def reset(self):
		self.scene, _ = scenic_helper.generateScene(self.scenario)

		if hasattr(self, "simulation"): self.simulation.get_underlying_gym_env().close()

		from scenic.simulators.gfootball.simulator import GFootBallSimulation
		self.simulation = GFootBallSimulation(scene=self.scene, settings={}, for_gym_env=True,
											  render=self.allow_render, verbosity=1,
											  env_type="v2",
											  gf_env_settings=self.gf_env_settings,
											  tag=str(self.rank))

		self.gf_gym_env = self.simulation.get_underlying_gym_env()
		return self.simulation.reset()

	def step(self, action):
		# Execute one time step within the environment
		return self.simulation.step(action)

	def render(self, mode='human', close=False):
		# Render the environment to the screen
		# For weird pygame rendering issue on Mac, rendering must be called in utilities/env_creator/create_environment
		return None


def render(self, mode='human', close=False):
	# Render the environment to the screen
	# For weird pygame rendering issue, rendering must be called in utilities/env_creator/create_environment
	return None


def test_env_v2():
	import os

	cwd = os.getcwd()

	gf_env_settings = {
		"stacked": True,
		"rewards": 'scoring',
		"representation": 'extracted',
		"players": [f"agent:left_players=1"],
		"real_time": True
	}

	from scenic.simulators.gfootball.rl.gfScenicEnv_v2 import GFScenicEnv_v2

	num_trials = 2
	scenario_file = f"/Users/azadsalam/codebase/scenic/examples/gfootball/monologue.scenic"
	scenario = buildScenario(scenario_file)

	env = GFScenicEnv_v2(initial_scenario=scenario, gf_env_settings=gf_env_settings, allow_render=True)

	from scenic.simulators.gfootball.rl import utils

	perf = utils.mean_reward_random_agent(env, num_trials=1)
	print("random agent performance: ", perf)

if __name__=="__main__":
	test_env_v2()