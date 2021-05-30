from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import OrderedDict
from gfootball.env import football_action_set
from typing import Dict, List

import gym
import pygame
import math
import gfootball
from gfootball.env import config
from gfootball.env import football_env
from scenic.simulators.gfootball.interface import update_objects_from_obs, generate_index_to_player_map, \
	update_control_index, update_objects_from_obs_single_rl_agent, update_index_ds
from scenic.simulators.gfootball.utilities import scenic_helper
from scenic.simulators.gfootball.utilities.constants import ActionCode
from scenic.simulators.gfootball.utilities.game_ds import GameDS
from scenic.simulators.gfootball.utilities.scenario_builder import initialize_gfootball_scenario#, get_default_settings
from scenic.syntax.veneer import verbosePrint
from scenic.core.simulators import Simulator, Simulation

import gfootball_engine as libgame
import scenic


class PlayerConfig:
	def __init__(self):
		#self.my_players =
		pass

class GameState:
	def __init__(self, game_mode:int = 0, score:List[int] = [0, 0], steps_left:int=-1, frame=None):
		self.frame = frame
		self.steps_left = steps_left
		self.score = score
		self.game_mode = game_mode


#One important implication is that there is a single action per 100 ms reported to the environment, which might cause a lag effect when playing.
class GFootBallSimulator(Simulator):
	def __init__(self, settings={}, render=True, record=False, timestep=None):
		super().__init__()
		verbosePrint('Connecting to GFootBall...')
		self.settings:Dict = None
		self.render = render
		self.timestep = timestep
		self.record = record


	def createSimulation(self, scene, verbosity=0):

		self.settings = scene.params.copy()

		"""
		verbosePrint(f"Parameters: ")
		for setting, option in self.settings.items():
			verbosePrint(f'{setting}: {self.settings[setting]}')
		"""
		return GFootBallSimulation(scene=scene, settings = self.settings,
								   timestep=self.timestep,
							   render=self.render, record=self.record,
							   verbosity=verbosity)


class GFootBallSimulation(Simulation):

	def __init__(self, scene, settings, timestep=None, render=False, record=False, verbosity=0, env_type = None, for_gym_env=False, gf_env_settings={}, tag=""):

		"""
		def __init__(self, scene, settings, timestep=None, render=False, record=False, verbosity=0, for_gym_env=False, gf_env_settings={},
					 use_scenic_behavior_in_step=False, constraints_checking=True, compute_scenic_actions=True, tag=""):
		"""


		super().__init__(scene, timestep=timestep, verbosity=verbosity)




		self.scene = scene
		self.verbosity = verbosity
		self.record = record
		self.timestep = timestep
		self.render = render
		#self.rewards = []
		self.last_raw_obs = None
		self.done = None
		self.for_gym_env = for_gym_env
		self.multi_player_rl = False

		self.settings = self.scene.params.copy()
		self.settings.update(settings)
		self.scenic_reward = None


		#assert not for_gym_env or use_scenic_behavior_in_step == constraints_checking,    "for now constraing checking has to be done when using scenic behavior"

		#MUST BE DONE TO CONFIGURE PLAYER SETTINGS FROM SCENIC PARAMETERS, FOR RL TRAINING, UPDATED PLAYER SETTINGS CAN BE PROVIDED via gf_env_settings

		self.gf_env_settings = self.settings.copy()
		self.tag = tag

		if gf_env_settings is not None:
			self.gf_env_settings.update(gf_env_settings)


		if env_type is not None:
			import scenic.syntax.veneer as veneer
			veneer.reset()
			self.init_run()

		"""Select environment modes"""

		self.env_type = env_type

		player_setting = None

		if env_type == "v2":

			for_gym_env = True
			self.for_gym_env = True
			self.run_pre_post_step = True
			#self.use_scenic_behavior_in_step = use_scenic_behavior_in_step
			self.constraints_checking = True
			self.compute_scenic_actions = True

			from scenic.simulators.gfootball.interface import is_my_player, is_op_player
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			num_op_player = len([obj for obj in scene.objects if is_op_player(obj)])

			internal_control_left = num_my_player
			internal_control_right = num_op_player

			player_setting = [f"agent:left_players={num_my_player},right_players={num_op_player}"]

		elif env_type == "v1":
			for_gym_env = True
			self.for_gym_env = True
			self.env_type = env_type

			#self.run_pre_post_step = False
			#self.constraints_checking = False
			#self.compute_scenic_actions = False

			internal_control_left = 1
			internal_control_right = 0

			player_setting = [f"agent:left_players=1"]

		elif env_type == "keyboard":
			self.env_type = env_type
			self.run_pre_post_step = False
			#self.use_scenic_behavior_in_step = use_scenic_behavior_in_step
			self.constraints_checking = False
			self.compute_scenic_actions = False

			#f"agent:left_players={num_my_player}", "keyboard:right_players=1"
			player_setting = [f"keyboard:right_players=1"]


		elif env_type is None:
			for_gym_env = False
			self.for_gym_env = False

			self.run_pre_post_step = True
			self.constraints_checking=True
			self.compute_scenic_actions=True

			from scenic.simulators.gfootball.interface import is_my_player, is_op_player
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			num_op_player = len([obj for obj in scene.objects if is_op_player(obj)])

			internal_control_left = num_my_player
			internal_control_right = num_op_player
			player_setting = [f"agent:left_players={num_my_player},right_players={num_op_player}"] #cannot be any space in the middle

		else:
			raise Exception


		self.gf_env_settings["players"] = player_setting
		self.gf_env_settings["internal_control_left"] = internal_control_left
		self.gf_env_settings["internal_control_right"] = internal_control_right


		self.env = self.create_gfootball_environment()

		if env_type is None:
			self.reset()



	"""
	def disable_rl_action(self):
		self.ignore_rl_action =  True

	def enable_rl_action(self):
		self.ignore_rl_action = False
	"""

	def create_gfootball_environment(self):
		from scenic.simulators.gfootball.utilities import env_creator

		self.game_ds: GameDS = self.get_game_ds(self.scene)
		level_name = initialize_gfootball_scenario(self.scene, self.game_ds, self.tag)
		#print("creating gfootball with level: ", level_name)
		#self.render=False
		#print("Game Level", self.gf_env_settings["level"])
		#print("gf level name", level_name)

		env, self.scenic_wrapper = env_creator.create_environment(env_name=level_name, settings=self.gf_env_settings, render=self.render)
		return env

	"""Initializes simulation from self.scene, in case of RL training a new scene is generated from self.scenario"""
	def reset(self):
		#if not self.first_time:
		#	self.env.close()
		#	self.env = self.create_gfootball_environment()
		#print("in simulator reset")
		#print("id self.env", id(self.env))
		#print("id scenic_wrapper", id(self.scenic_wrapper))

		obs = self.env.reset()
		self.last_raw_obs = self.scenic_wrapper.latest_raw_observation
		#print(self.last_raw_obs[0]['active'])
		#print("id last_obs", id(self.scenic_wrapper.latest_raw_observation))
		#print(f"game_ds", id(self.game_ds))
		#print("in simulator: ball: ", self.last_raw_obs[0]["ball"])
		#print("In Reset Simulation")
		#self.game_ds.print_mini()

		if self.env_type == "v1": #		if self.for_gym_env:
			#assert not self.multi_player_rl, "Multi Player Rl has not been tested yet."
			update_index_ds(self.last_raw_obs, gameds=self.game_ds)
			update_objects_from_obs_single_rl_agent(self.last_raw_obs, self.game_ds)
			self.update_designated_player()
		else:
			update_control_index(self.last_raw_obs, gameds=self.game_ds)
			update_objects_from_obs(self.last_raw_obs, self.game_ds)
			self.update_designated_player()

		#print("AT reset in simulation: Ball: ", self.game_ds.ball.position)
		self.done = False

		#self.first_time = False
		return obs

	"""
		def initialize_multiplayer_ds(self, obs):
			self.multiplayer = True
			self.num_controlled = len(obs)
		"""

	def get_game_ds(self, scene):

		game_state = GameState()
		my_players = []
		op_players = []

		"""Extracts Ball and Players"""
		# from scenic.simulators.gfootball import model
		from scenic.simulators.gfootball.interface import is_player, is_ball, is_op_player, is_my_player
		for obj in self.objects:
			if is_ball(obj):
				ball = obj

			elif is_my_player(obj):
				my_players.append(obj)

			elif is_op_player(obj):
				op_players.append(obj)

		return GameDS(my_players, op_players, ball=ball, game_state=game_state, scene=scene)

	"""
	def get_player_settings(self, scene, agent_left, agent_right,):

		from scenic.simulators.gfootball.interface import is_my_player, is_op_player
		num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
		num_op_player = len([obj for obj in scene.objects if is_op_player(obj)])

		return [f"agent:left_players={num_my_player}", "keyboard:right_players=1"]
	"""
	def configure_player_settings(self, scene):

		from scenic.simulators.gfootball.interface import is_my_player, is_op_player
		manual_control = scene.params["manual_control"]

		# If used for gym environment, this player settings will be overriden by gf_env_settting in __init__
		# if manual control is enabled, the op player wont be allowed to have any scenic behaviors for now
		if manual_control:
			op_players = [obj for obj in scene.objects if is_op_player(obj)]
			opp_with_bhv = [obj for obj in op_players if obj.behavior is not None]
			assert len(
				opp_with_bhv) == 0, "For now, if manual control is enabled, the opposition players cannot have scenic behaviors"

			# ALL MY_PLAYER WILL BE controlled by `agent` i.e., the simulator expects actions for every agent
			# the opposition will be controlled by keyboard
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			self.settings["players"] = [f"agent:left_players={num_my_player}", "keyboard:right_players=1"]

		else:
			# ALL MY_PLAYERs and OPPLAYES are controlled by `agent` i.e., the simulator expects actions for every agent
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			num_op_player = len([obj for obj in scene.objects if is_op_player(obj)])

			self.settings["players"] = [f"agent:left_players={num_my_player}, right_players={num_op_player}"]


	def get_base_gfootball_env(self):
		return self.env

	def get_underlying_gym_env(self):
		return self.env

	def executeActions(self, allActions):
		gameds = self.game_ds

		#when no behavior is specified, built in AI takes charge
		self.actions = [football_action_set.action_builtin_ai] * gameds.get_num_controlled()

		"""
		if self.for_gym_env:
			assert not self.multi_player_rl, "Multi Player Rl has not been tested yet."
			controlled_player = self.game_ds.controlled_player
			self.action = ActionCode.builtin_ai
			if controlled_player in allActions:
				self.action = allActions[controlled_player][0].code
				#print(self.game_ds.player_str_mini(controlled_player), self.action)

			#print(self.game_ds.player_str_mini(controlled_player), self.action)
		else:
		"""
		"""
		if self.env_type=="v1":
			designated_player = self.game_ds.designated_player
			if designated_player in allActions:
				self.action = allActions[designated_player][0].code

		elif self.env_type=="v2":
			for agent, act in allActions.items():
				idx = gameds.player_to_ctrl_idx[agent]
				self.actions[idx] = act[0].code

		elif not self.for_gym_env:
			for agent, act in allActions.items():
				idx = gameds.player_to_ctrl_idx[agent]
				self.actions[idx] = act[0].code
		"""

		if self.env_type=="v2" or not self.for_gym_env:
			for agent, act in allActions.items():
				idx = gameds.player_to_ctrl_idx[agent]
				self.actions[idx] = act[0].code

		elif self.env_type=="v1":
			designated_player = self.game_ds.designated_player
			self.designated_player_action = allActions[designated_player][0].code


	def get_actions(self):
		return self.actions

	def get_scenic_designated_player_action(self):
		if self.env_type == "v1":
			return self.designated_player_action
		else:
			return self.actions[self.game_ds.designated_player_idx]

	def update_designated_player(self):
		if self.env_type == "v1":
			pass
		else:
			self.game_ds.compute_designated_as_closest_idx()

	def get_controlled_player_idx(self):

		#if self.env_type == "v1":
		#	idx = self.game_ds.controlled_player

		idx = self.game_ds.get_designated_player_idx()
		#idx = self.game_ds.compute_designated_player_idx()

		return idx




	def step(self, action=None):

		#if self.run_pre_post_step:
		#	new_done = self.pre_step()
		#	#TODO if simulation ended for constraints handle it

		#input()
		#print("in step")
		# Run simulation for one timestep
		if self.done:
			#TODO: how to signal end of simulation
			#print(f"Reward Sum: {sum(self.rewards)}")
			self.env.close()

			#if self.for_gym_env:
			#the code may not ever come here for gym ??
			assert not self.for_gym_env, "Must not come here ??"

			return 0

			#signal scenic backend to stop simulation
			#askEddie: Signal end of simulation


		if action==None:
			assert not self.for_gym_env
			action_to_take = self.actions
		else:
			action_to_take = action


		"""
		if self.for_gym_env and not self.use_scenic_behavior_in_step:
			#TODO: For now pass whatever the RL training is passing, however when training with scenarios having agents using scenic behavior it may needed to be changed
			action_to_take = action
		else:
			action_to_take = self.actions
		"""

		#print(action_to_take)
		obs, sim_rew, self.done, info = self.env.step(action_to_take)
		info["action_taken"] = action_to_take
		self.last_action = action_to_take
		self.last_raw_obs = self.scenic_wrapper.latest_raw_observation

		#print(self.last_raw_obs[0]['active'])

		#self.rewards.append(rew)


		if self.env_type == "v1":
			#clean up after simulation ended
			#if self.done and self.run_pre_post_step:
			#	self.post_run()
			#assert not self.multi_player_rl, "Multi Player Rl has not been tested yet."
			update_objects_from_obs_single_rl_agent(self.last_raw_obs, self.game_ds)
			self.update_designated_player()
		else:
			update_objects_from_obs(self.last_raw_obs, self.game_ds)
			self.update_designated_player()

		total_rew = sim_rew
		self.calculate_reward()
		if self.scenic_reward is not None:
			scenic_reward = self.scenic_reward
			total_rew += scenic_reward
			#print(f"{self.timestep}: scenic_reward: ", scenic_reward, "total reward: ", total_rew)

		"""
		print("Printing objects")
		for obj in self.objects:
			print(obj, obj.position)
		print("*" * 80)
		print()
		"""
		#if self.for_gym_env:
		#	self.post_step()

		#self.game_ds.print_mini()

		if self.env_type is not None and self.done:
			self.post_run()

		if self.for_gym_env:
			return obs, total_rew, self.done, info

		else:
			return None


		#input()



	def getProperties(self, obj, properties):
		# Extract  properties

		values = dict()
		if obj == self.game_ds.ball:
			# ball dynamic properties

			#5 gfootball properties: position, direction, rotation, owned_team, owned_player
			values['position'] = obj.position
			values['direction'] = obj.direction
			values['rotation'] = obj.rotation                     #UNPROCESSED #TODO: Process Rotation ?
			values['owned_team'] = obj.owned_team
			values['owned_player_idx'] = obj.owned_player_idx     #TODO: Test it How ??

			# scenic defaults
			values['angularSpeed'] = obj.angularSpeed			  #UNPROCESSED / NO VALUE
			values['heading'] = obj.heading					      #same as direction
			values['speed'] = obj.speed							#TODO: test this value
			values['velocity'] = obj.velocity
			#print(f"ball position {values['position']}")

		elif obj in self.game_ds.my_players or obj in self.game_ds.op_players:

			values['position'] = obj.position
			values['direction'] = obj.direction
			values['tired_factor'] = obj.tired_factor
			values['yellow_cards'] = obj.yellow_cards		#todo: need to test it
			values['red_card'] = obj.red_card				#todo: need to test it
			values['role'] = obj.role
			#values['controlled'] = obj.controlled
			if hasattr(obj, "is_controlled"):
				values['is_controlled'] = obj.is_controlled
			else:
				values['is_controlled'] = False
			values['owns_ball'] = obj.owns_ball
			values['sticky_actions'] = obj.sticky_actions

			values['velocity'] = obj.velocity
			values['angularSpeed'] = obj.angularSpeed        #unspecified
			values['speed'] = obj.speed
			values['heading'] = obj.direction
		else:
			values['velocity'] = 0
			values['angularSpeed'] = obj.angularSpeed
			values['position'] = obj.position
			values['speed'] = 0
			values['heading'] = 0


		return values

if __name__ == "__main__":
	g = GFootBallSimulator()
	s = g.createSimulation(None)
	#g.simulate()
