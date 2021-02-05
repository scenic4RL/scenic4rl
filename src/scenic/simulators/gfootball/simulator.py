from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, List

import gym
import pygame
import math
import gfootball
from gfootball.env import config
from gfootball.env import football_env
from scenic.simulators.gfootball.interface import update_objects_from_obs, generate_index_to_player_map, \
	update_control_index
from scenic.simulators.gfootball.utilities import scenic_helper
from scenic.simulators.gfootball.utilities.game_ds import GameDS
from scenic.simulators.gfootball.utilities.scenario_builder import initialize_gfootball_scenario, get_default_settings
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


		verbosePrint(f"Parameters: ")
		for setting, option in self.settings.items():
			verbosePrint(f'{setting}: {self.settings[setting]}')

		return GFootBallSimulation(scene=scene, settings = self.settings,
								   timestep=self.timestep,
							   render=self.render, record=self.record,
							   verbosity=verbosity)


class GFootBallSimulation(Simulation):

	def __init__(self, scene, settings, timestep=None, render=True, record=False, verbosity=0, for_gym_env=False, gf_env_settings={}):

		super().__init__(scene, timestep=timestep, verbosity=verbosity)

		self.scene = scene
		self.verbosity = verbosity
		self.record = record
		self.timestep = timestep
		self.settings = settings
		self.rewards = []
		self.last_obs = None
		self.done = None
		self.for_gym_env = for_gym_env

		self.settings = self.scene.params.copy()

		if for_gym_env:
			self.gf_env_settings = gf_env_settings
		else:
			self.gf_env_settings = self.settings


		self.env = self.create_gfootball_environment()

		if not for_gym_env:
			self.reset()


	def create_gfootball_environment(self):
		from scenic.simulators.gfootball.utilities import env_creator

		self.configure_player_settings(self.scene)
		self.game_ds: GameDS = self.get_game_ds(self.scene)
		initialize_gfootball_scenario(self.scene, self.game_ds)

		env = env_creator.create_environment(env_name=self.gf_env_settings["level"], settings=self.gf_env_settings)
		return env

	"""Initializes simulation from self.scene, in case of RL training a new scene is generated from self.scenario"""
	def reset(self):

		self.last_obs = self.env.reset()

		update_control_index(self.last_obs, gameds=self.game_ds)
		update_objects_from_obs(self.last_obs, self.game_ds)
		self.done = False

		return self.last_obs

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

	def configure_player_settings(self, scene):

		from scenic.simulators.gfootball.interface import is_my_player, is_op_player
		manual_control = scene.params["manual_control"]

		# if manual control is enabled, the op player wont be allowed to have any scenic behaviors for now
		if manual_control:
			op_players = [obj for obj in scene.objects if is_op_player(obj)]
			opp_with_bhv = [obj for obj in op_players if obj.behavior is not None]
			assert len(
				opp_with_bhv) == 0, "For now, if manual control is enabled, the opposition players cannot have scenice behaviors"

			# ALL MY_PLAYER WILL BE controlled by `agent` i.e., the simulator expects actions for every agent
			# the opposition will be controlled by keyboard
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			self.settings["players"] = [f"agent:left_players={num_my_player}", "keyboard:right_players=1"]

		else:
			# ALL MY_PLAYERs and OPPLAYES are controlled by `agent` i.e., the simulator expects actions for every agent
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			num_op_player = len([obj for obj in scene.objects if is_op_player(obj)])

			self.settings["players"] = [f"agent:left_players={num_my_player},right_players={num_op_player}"]



	def get_base_gfootball_env(self):
		return self.env

	def get_underlying_gym_env(self):
		return self.env

	def executeActions(self, allActions):
		gameds = self.game_ds
		self.action = [-1] * gameds.get_num_controlled()


		for agent, act in allActions.items():
			idx = gameds.player_to_ctrl_idx[agent]
			self.action[idx] = act[0].code



	#askEddie: How to Report end of an episode (i.e., simulation????)
	def step(self):
		#input()
		#print("in step")
		# Run simulation for one timestep
		if self.done:
			#self.last_obs = self.env.reset()
			#self.done = False
			print(f"Reward Sum: {sum(self.rewards)}")
			return sum(self.rewards)
			#self.endSimulation()
			#signal scenic backend to stop simulation

			#raise Exception
			#askEddie: Signal end of simulation

		self.last_obs, rew, self.done, info = self.env.step(self.action)
		self.rewards.append(rew)

		update_objects_from_obs(self.last_obs, self.game_ds)

		if self.for_gym_env:
			return self.last_obs, rew, self.done, info

		else:
			return None

		#self.game_ds.print_ds()
		#input()

		#update_objects_from_obs(self.last_obs, self.objects, self.game_state, self.my_player_to_idx, self.my_idx_to_player, self.op_player_to_idx, self.op_idx_to_player, self.num_controlled)

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

		elif obj in self.game_ds.my_players or obj in self.game_ds.op_players:

			values['position'] = obj.position
			values['direction'] = obj.direction
			values['tired_factor'] = obj.tired_factor
			values['yellow_cards'] = obj.yellow_cards		#todo: need to test it
			values['red_card'] = obj.red_card				#todo: need to test it
			values['role'] = obj.role
			#values['controlled'] = obj.controlled
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
