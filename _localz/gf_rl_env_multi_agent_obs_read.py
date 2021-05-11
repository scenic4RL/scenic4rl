from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from gfootball.env.scenario_builder import Scenario
from gfootball.env import config
import gfootball.env as football_env

import gfootball_engine as libgame
from gfootball.env import football_action_set

# AddPlayer(self, x, y, role, lazy=False, controllable=True):
num_my_player = 2
num_op_player = 2
num_total_controlled = num_my_player + num_op_player

level = "5_vs_5"
#        rewards="",
#number_of_left_players_agent_controls=num_my_player,
#	number_of_right_players_agent_controls = num_op_player
#

def print_obs(obs):

	if len(obs.shape)==4:
		for i in range(obs.shape[0]):
			print("obs index: ",i)
			left_team, right_team, ball, active_player = read_single_obs(obs[i])
			#print("Left Team: ", left_team)
			#print("Right Team: ", right_team)
			print("Ball: ", ball)
			print("Active: ", active_player)
			print("--"*80)
	else:
		print("si")
		read_single_obs(obs)
		print("--" * 80)

def read_single_obs(obs):

	import numpy as np


	def get_pos(plane):
		pos = []
		nz = np.nonzero(plane)
		n = int(nz[0].shape[0])
		for i in range(n):
			x = nz[0][i]
			y = nz[1][i]
			pos.append((x,y))
		return pos

	last_frame = obs[:, :, -4:]

	left_plane = last_frame[:, :, 0]
	left_team = get_pos(left_plane)

	right_team = get_pos(last_frame[:,:,1])
	ball = get_pos(last_frame[:,:,2])
	active_player = get_pos(last_frame[:,:,3])

	"""
	print("Left Team: ", left_team)
	print("Right Team: ", right_team)
	print("Ball: ", ball)
	print("Active: ", active_player)
	"""
	return left_team, right_team, ball, active_player




env = football_env.create_environment(
	env_name=level,
	stacked=True,
	number_of_left_players_agent_controls=num_my_player,
	number_of_right_players_agent_controls = num_op_player
)
env.render()
env.reset()
obs, rew, done, info = env.step([0] * num_total_controlled)
print_obs(obs)
#quit()
#print(obs["active"], obs["designated"])
while True:
    obs, res, done, info = env.step([football_action_set.action_shot] * num_total_controlled)
    print("step")
    print_obs(obs)
    #_, _, done, _ = env.step([])
    if done:
        break
