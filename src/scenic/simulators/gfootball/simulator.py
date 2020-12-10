from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, List
import math
import gfootball
from gfootball.env import config
from gfootball.env import football_env
from scenic.simulators.gfootball.interface import update_objects_from_obs
from scenic.simulators.gfootball.utilities.scenario_builder import initialize_gfootball_scenario, get_default_settings

from scenic.syntax.translator import verbosity

from scenic.core.simulators import SimulationCreationError
from scenic.syntax.veneer import verbosePrint
from scenic.core.simulators import Simulator, Simulation

import gfootball_engine as libgame
#Player = libgame.FormationEntry
#Role = libgame.e_PlayerRole
#Team = libgame.e_Team

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
		self.settings:Dict = settings
		self.render = render
		self.timestep = timestep
		self.record = record

		default_settings = {
			'action_set': "full",
			'dump_full_episodes': False,
			'real_time': True,
			'players': ['agent:left_players=1']
		}

		for setting, option in default_settings.items():
			if setting not in self.settings:
				verbosePrint(f'Using Default Settings for {setting}: {default_settings[setting]}')
				self.settings[setting] = default_settings[setting]

	def createSimulation(self, scene, verbosity=0):
		return GFootBallSimulation(scene=scene, settings = self.settings,
								   timestep=self.timestep,
							   render=self.render, record=self.record,
							   verbosity=verbosity)




class GFootBallSimulation(Simulation):

	def initialize_utility_ds(self):
		self.game_state = GameState()
		"""Initializes self.ball, self.my_players and self.opo_players"""
		from scenic.simulators.gfootball import model
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

		Player = libgame.FormationEntry
		Role = libgame.e_PlayerRole
		Team = libgame.e_Team

		self.initialize_utility_ds()
		initialize_gfootball_scenario(scene, self.objects)
		settings = get_default_settings()
		self.settings.update(settings)

		print("New Simulation")
		#SET UP CONFIG
		self.cfg = config.Config(self.settings)

		self.env = football_env.FootballEnv(self.cfg)
		self.render = render

		if self.render:
			self.env.render()

		self.last_obs = self.env.reset()

		#input()
		self.done = False

		#obs = self.last_obs[0]

		update_objects_from_obs(self.last_obs, self.objects, self.game_state)



	def executeActions(self, allActions):

		self.action = [0]
		for agent, act in allActions.items():
			if agent.controlled:
				self.action = [act[0].code]
				#print(f"In simulator: Taking {act[0]} action")
				#input("In simulator: Step?")



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
		update_objects_from_obs(self.last_obs, self.objects, self.game_state)


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
