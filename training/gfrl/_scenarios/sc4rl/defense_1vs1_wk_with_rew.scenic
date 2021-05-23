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
	tstep = 0
	sim = simulation()
	gameds = sim.game_ds
	RLTeamTakesPossession = False
	#OpTeamScoresAtLeastOnce = False

	op_shot_attempted = False
	rl_shot_attempted = False

	while True:
		ball = gameds.ball
		#if tstep<2:
		#	print(f"ball at t = {tstep}  :", ball.position)
			#	print(f"tstep: 0 op_shot_attempted: ", op_shot_attempted)
		#	tstep += 1
		scenic_reward = 0
		# Case 1: Opponent Team Scores: No need in case of shaping
		#if opTeamScored:
			# sim.scenic_reward += -1
		#	OpTeamScoresAtLeastOnce = True

		# Case 2: Opponent Team takes a shot, may/may not scored: -0.5
		# I took out the condition about "once" because the simulation will terminate if the ball goes off the field
		#print("ball: ", ball.position)
		#PROBLEM: sometimes after 97/98 it the ball doesnt go <-100 but restarts.
		#PROBLEM 2: Goal Kick / Back Pass case

		if ball.position.x <= -95 and abs(ball.position.y) < 10 and not op_shot_attempted:
			#print("goal attempted??: ",  op_shot_attempted)

			#print("Opponent Shot")
			#if :
			op_shot_attempted = True
			scenic_reward += -0.75

		# Case 3: RL Team Scores : No need in case of shaping
		#if RLTeamScored:
		#	sim.scenic_reward += 1

		# Case 4: RL Agent Team takes a shot, may/may not score: +0.5
		if ball.position.x >= 95 and abs(ball.position.y) < 10 and not rl_shot_attempted:
			rl_shot_attempted = True
			#print("My Shot")
			scenic_reward += 0.5

		# Case 5: If RL Agent Team never takes possession of the ball by the end of the simulation, -0.5
		#print("ball owned team:",gameds.ball.owned_team )
		if gameds.ball.owned_team == 0:
			#print("RL Team takes possession")
			RLTeamTakesPossession = True

		if sim.done and not RLTeamTakesPossession:
			#print("RL never possessed the ball")
			scenic_reward += -0.5

		#if sim.done:
		#	print("ball pos final: ", ball.position)
		#Problem: Cancels out RL Team not possessing Ball
		# Case 6: If RL Team did not concede a goal in defense by the end of the simulation: +0.5
		#if sim.done and  gameds.game_state.score[1] == 0:
		#	print("No goal conceded")
		#	scenic_reward += 0.5

		#prev_RLTeamScore = gameds.game_state.score[0]
		#prev_opTeamScore = gameds.game_state.score[1]

		sim.scenic_reward = scenic_reward

		wait

"""
monitor reward_function:
	step = 0
	sim = simulation()
	gameds = sim.game_ds
	once = False
	while True:
		#ba;; = sim.game_ds.
		#print(ball.owned_team)
		print(gameds.game_state.score, sim.done)
		my_score = gameds.game_state.score[0]
		op_score = gameds.game_state.score[1]
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
"""