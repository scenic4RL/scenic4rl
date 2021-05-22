from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True



MyGK at -98 @ 0
yellow_defender = MyRB

#left_goal_nearby = get_reg_from_edges(-100, -90, 20, -20)
reg = get_reg_from_edges(-75, -85, 2, -2)

OpGK at 98 @ 0
ego = OpCF on LeftReg_CB, facing 90 deg

ball = Ball ahead of ego by 4

monitor reward_function:
	step = 0
	sim = simulation()
	gameds = sim.game_ds
	once = False
	while True:
		#ba;; = sim.game_ds.
		#print(ball.owned_team)
		#print(ball.position)
		if ball.position[0]<=-90 and abs(ball.position[1])<10 and not once:
			sim.scenic_reward = -0.5
			once = True
		else:
			sim.scenic_reward = 0


		#print(sim.last_action)
		#ball_position =
		#= step
		#step += 1
		wait
