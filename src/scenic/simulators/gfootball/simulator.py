from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, List
import math
import gfootball
from gfootball.env import config
from gfootball.env import football_env
from scenic.simulators.gfootball.interface import update_objects_from_obs, generate_index_to_player_map
from scenic.simulators.gfootball.utilities.scenario_builder import initialize_gfootball_scenario, get_default_settings
from scenic.syntax.veneer import verbosePrint
from scenic.core.simulators import Simulator, Simulation

import gfootball_engine as libgame


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

		from scenic.simulators.gfootball.interface import is_my_player, is_op_player
		self.settings = scene.params.copy()

		manual_control = scene.params["manual_control"]

		#if manual control is enabled, the op player wont be allowed to have any scenic behaviors for now
		if manual_control:
			op_players = [obj for obj in scene.objects if is_op_player(obj)]
			opp_with_bhv = [obj for obj in op_players if obj.behavior is not None]
			assert len(opp_with_bhv)==0, "For now, if manual control is enabled, the opposition players cannot have scenice behaviors"


			#ALL MY_PLAYER WILL BE controlled by `agent` i.e., the simulator expects actions for every agent
			# the opposition will be controlled by keyboard
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			self.settings["players"] = [f"agent:left_players={num_my_player}", "keyboard:right_players=1"]

		else:
			# ALL MY_PLAYERs and OPPLAYES are controlled by `agent` i.e., the simulator expects actions for every agent
			num_my_player = len([obj for obj in scene.objects if is_my_player(obj)])
			num_op_player = len([obj for obj in scene.objects if is_op_player(obj)])

			self.settings["players"] = [f"agent:left_players={num_my_player},right_players={num_op_player}"]

		verbosePrint(f"Parameters: ")
		for setting, option in self.settings.items():
			verbosePrint(f'{setting}: {self.settings[setting]}')

		return GFootBallSimulation(scene=scene, settings = self.settings,
								   timestep=self.timestep,
							   render=self.render, record=self.record,
							   verbosity=verbosity)


class GFootBallSimulation(Simulation):

	def initialize_multiplayer_ds(self, obs):
		self.multiplayer = True
		self.num_controlled = len(obs)

	def initialize_utility_ds(self):

		self.multiplayer = False
		self.game_state = GameState()

		"""Initializes self.ball, self.my_players and self.opo_players"""
		#from scenic.simulators.gfootball import model
		from scenic.simulators.gfootball.interface import is_player, is_ball, is_op_player, is_my_player
		for obj in self.objects:
			if is_ball(obj):
				self.ball = obj

			elif is_my_player(obj):
				self.my_players.append(obj)

			elif is_op_player(obj):
				self.opo_players.append(obj)



	def __init__(self, scene, settings, timestep=0.1, render=True, record=False, verbosity=0):
		super().__init__(scene, timestep=timestep, verbosity=verbosity)
		self.verbosity = verbosity
		self.record = record
		self.timestep = timestep
		self.scene = scene
		self.settings = settings
		self.rewards = []
		self.last_obs = None

		#DS for accessing easily
		self.ball = None
		self.my_players = []
		self.opo_players = []

		self.initialize_utility_ds()
		initialize_gfootball_scenario(scene, self.objects)

		print("New Simulation")
		#SET UP CONFIG
		self.cfg = config.Config(self.settings)

		self.env = football_env.FootballEnv(self.cfg)
		self.render = render

		if self.render:
			self.env.render()

		self.last_obs = self.env.reset()
		self.my_player_to_idx, self.my_idx_to_player, self.op_player_to_idx, self.op_idx_to_player = generate_index_to_player_map(self.last_obs, self.objects)
		self.initialize_multiplayer_ds(self.last_obs)

		#input()
		self.done = False

		#obs = self.last_obs[0]

		update_objects_from_obs(self.last_obs, self.objects, self.game_state, self.my_player_to_idx, self.my_idx_to_player, self.op_player_to_idx, self.op_idx_to_player, self.num_controlled)



	def executeActions(self, allActions):

		self.action = [-1] * self.num_controlled

		for agent, act in allActions.items():
			idx = self.my_player_to_idx[agent]
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

		self.last_obs, rew, self.done, _ = self.env.step(self.action)
		self.rewards.append(rew)
		update_objects_from_obs(self.last_obs, self.objects, self.game_state, self.my_player_to_idx, self.my_idx_to_player, self.op_player_to_idx, self.op_idx_to_player, self.num_controlled)


	#askEddie: How to use this function? Where are these properties set, why only one obj
	#to test this we need behaviors
	def getProperties(self, obj, properties):
		# Extract  properties

		values = dict()
		if obj == self.ball:
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
			values['speed'] = obj.speed
			values['velocity'] = obj.velocity

		elif obj in self.my_players or obj in self.opo_players:

			values['position'] = obj.position
			values['direction'] = obj.direction
			values['tired_factor'] = obj.tired_factor
			values['yellow_cards'] = obj.yellow_cards		#todo: need to test it
			values['red_card'] = obj.red_card				#todo: need to test it
			values['role'] = obj.role
			values['controlled'] = obj.controlled
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
