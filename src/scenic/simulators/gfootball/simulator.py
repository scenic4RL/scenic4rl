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
	def __init__(self, scene, settings, timestep=0.1, render=True, record=False, verbosity=0):
		super().__init__(scene, timestep=timestep, verbosity=verbosity)
		self.verbosity = verbosity
		self.record = record
		self.timestep = timestep
		self.scene = scene
		self.settings = settings
		self.rewards = []
		self.last_obs = None


		self.ball = None
		self.my_players = []
		self.opo_players = []

		Player = libgame.FormationEntry
		Role = libgame.e_PlayerRole
		Team = libgame.e_Team


		initialize_gfootball_scenario(scene, self.objects)
		settings = get_default_settings()
		self.settings.update(settings)

		#SET UP CONFIG
		self.cfg = config.Config(self.settings)

		self.env = football_env.FootballEnv(self.cfg)
		self.render = render

		if self.render:
			self.env.render()

		self.last_obs = self.env.reset()
		self.done = False

		#obs = self.last_obs[0]

		update_objects_from_obs(self.last_obs, self.objects)


		#read observation

		#obs index to <-> player role : loop over left_team roles



		#APplies "control" to carla objects

		#Set Carla actor's initial speed (if specified)


	def executeActions(self, allActions):
		#Apply control updates which were accumulated while executing the actions
		#for openai gym execute action is part of step ??
		#does this only buffer all sort of actions ????

		self.action = [0]
		for agent, act in allActions.items():
			if agent.active:
				self.action = [act[0].code]
				print(f"In simulator: Taking {act} actions")



	#askEddie: How to Report end of an episode (i.e., simulation????)
	def step(self):
		# Run simulation for one timestep
		if self.done:
			self.last_obs = self.env.reset()
			self.done = False
			print(f"Reward Sum: {sum(self.rewards)}")
			#askEddie: Signal end of simulation

		self.last_obs, rew, self.done, _ = self.env.step(self.action)
		self.rewards.append(rew)
		update_objects_from_obs(self.last_obs, self.objects)


	#askEddie: How to use this function? Where are these properties set, why only one obj
	def getProperties(self, obj, properties):
		# Extract  properties
		values = dict()
		values['velocity'] = 0
		values['angularSpeed'] = self.last_obs
		values['position'] = obj.position
		values['speed'] = 0
		values['heading'] = 0
		return values

if __name__ == "__main__":
	g = GFootBallSimulator()
	s = g.createSimulation(None)
	#g.simulate()
