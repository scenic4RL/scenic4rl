from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, List
import math

from gfootball.env import config
from gfootball.env import football_env

from scenic.syntax.translator import verbosity

from scenic.core.simulators import SimulationCreationError
from scenic.syntax.veneer import verbosePrint
from scenic.core.simulators import Simulator, Simulation


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
			'players': ['keyboard:left_players=1']
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
	def __init__(self, scene, settings, timestep, render, record, verbosity=0):
		super().__init__(scene, timestep=timestep, verbosity=verbosity)
		self.verbosity = verbosity
		self.record = record
		self.timestep = timestep
		self.scene = scene
		self.settings = settings
		self.cfg = config.Config(self.settings)

		self.env = football_env.FootballEnv(self.cfg)
		self.render = render

		if self.render:
			self.env.render()
		self.env.reset()

		#Reloads current world: destroys all actors, except traffic manager instances == ?
		#connects display if render == true


		#Create Carla actors corresponding to Scenic objects
		#need blueprint ?
		#set transforms (location and rotations)
		#


		#DO THE FIRST TICK/STEP


		#APplies "control" to carla objects

		#Set Carla actor's initial speed (if specified)

	def executeActions(self, allActions):
		#Apply control updates which were accumulated while executing the actions
		#for openai gym execute action is part of step ??
		#does this only buffer all sort of actions ????
		pass

	def step(self):
		# Run simulation for one timestep
		self.env.step([])

	def getProperties(self, obj, properties):
		# Extract  properties
		values = dict()
		values['velocity'] = 0
		values['angularSpeed'] = 0
		values['position'] = 0
		values['speed'] = 0
		values['heading'] = 0
		# {'velocity', 'angularSpeed', 'position', 'speed', 'heading'
		return values

if __name__ == "__main__":
	g = GFootBallSimulator()
	s = g.createSimulation(None)
	#g.simulate()
