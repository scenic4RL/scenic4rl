from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, List
import math
import gfootball
from gfootball.env import config
from gfootball.env import football_env

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
	def __init__(self, scene, settings, timestep=0.1, render=True, record=False, verbosity=0):
		super().__init__(scene, timestep=timestep, verbosity=verbosity)
		self.verbosity = verbosity
		self.record = record
		self.timestep = timestep
		self.scene = scene
		self.settings = settings

		Player = libgame.FormationEntry
		Role = libgame.e_PlayerRole
		Team = libgame.e_Team

		def get_scenario_python_str(scene_attrs, own_players, opo_players, ball):
			code_str = ""
			code_str += "from . import *\n"

			code_str += "def build_scenario(builder):\n"

			# basic settings:
			for name, value in scene_attrs.items():
				code_str += f"\tbuilder.config().{name} = {value}\n"

			# add Ball
			code_str += f"\tbuilder.SetBallPosition({ball.position.x}, {ball.position.y})\n"

			# addOwnPlayers:
			code_str += f"\tbuilder.SetTeam(Team.e_Left)\n"

			for player in own_players:
				code_str += f"\tbuilder.AddPlayer({player.position.x}, {player.position.y}, e_PlayerRole_{player.role})\n"

			code_str += "\n"
			code_str += "\n"

			# addOponentPlayers:
			code_str += f"\tbuilder.SetTeam(Team.e_Right)\n"

			for player in opo_players:
				code_str += f"\tbuilder.AddPlayer({player.position.x}, {player.position.y}, e_PlayerRole_{player.role})\n"

			code_str += "\n"
			code_str += "\n"

			return code_str

		# write scenario to file
		GFOOTBALL_SCENARIO_FILENAME = "dynamic.py"

		def initialize_gfootball_scenario():

			# set basic scenario attributes

			scene_attrs = {}

			default_scene_params = {
				'game_duration': 400,
				'deterministic': False,
				'offsides': False,
				'end_episode_on_score': True,
				'end_episode_on_out_of_play': False,
				'end_episode_on_possession_change': False,
				'right_team_difficulty': 0.0,
				'left_team_difficulty': 0.0
			}

			#Set default parameters for scene
			scene_attrs.update(default_scene_params)

			#UPDATE SCENE PARAMETERS
			scene_attrs.update(scene.params)

			module_path = gfootball.scenarios.__path__[0]

			from scenic.simulators.gfootball.model import Player, Ball
			ball = None
			my_players = []
			op_players = []
			for obj in self.objects:
				print(obj, type(obj))

				# change with isinstance
				if "MyPlayer" in str(type(obj)):
					my_players.append(obj)

				elif "OpPlayer" in str(type(obj)):
					op_players.append(obj)

				elif "Ball" in str(type(obj)):
					# print(f"Ball {dir(obj)}")
					ball = obj

			print(f"...Writing GFootBall Scenario to {module_path}")

			with open(module_path + "/" + GFOOTBALL_SCENARIO_FILENAME, "w+") as file:
				code_str = get_scenario_python_str(scene_attrs, own_players=my_players, opo_players=op_players, ball=ball)
				print(code_str)
				file.write(code_str)

		initialize_gfootball_scenario()
		settings = {
			'action_set': "full",
			'dump_full_episodes': False,
			'real_time': True,
			'players': ['keyboard:left_players=1'],
			'level': GFOOTBALL_SCENARIO_FILENAME[:-3]
		}

		self.settings.update(settings)



		#SET UP CONFIG
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
