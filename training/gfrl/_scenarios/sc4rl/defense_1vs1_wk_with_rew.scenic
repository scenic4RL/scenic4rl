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



MyGK at 98 @ 0
yellow_defender = MyRB

#left_goal_nearby = get_reg_from_edges(-100, -90, 20, -20)
reg = get_reg_from_edges(-75, -85, 2, -2)

OpGK at 98 @ 0
ego = OpCF on LeftReg_CB, facing 90 deg

ball = Ball ahead of ego by 4


def rlTeamTakesPossession():
    ''' this includes case when the player itself has the ball possession '''
    for p in simulation().objects:
        if not isinstance(p, Ball) and p.team == 'RLteam' and p.owns_ball:
            return True
    return False


monitor reward_function:
	sim = simulation()
	gameds = sim.game_ds
	RLTeamTakesPossession = False
	OpTeamScoresAtLeastOnce = False

	prev_RLTeamScore = 0
	prev_opTeamScore = 0
	while True:
		RLTeamScored = prev_RLTeamScore + 1 == gameds.game_state.score[0]
		opTeamScored = prev_opTeamScore + 1 == gameds.game_state.score[1]

		# Case 1: Opponent Team Scores
		if opTeamScored:
			#sim.scenic_reward += -1
			OpTeamScoresAtLeastOnce = True

		# Case 2: Opponent Team takes a shot but misses scoring: -0.5
		# I took out the condition about "once" because the simulation will terminate if the ball goes off the field
		if not RLTeamScored and ball.position.x <= -100 and abs(ball.position.y) < 10 and not once:
			sim.scenic_reward += -0.5

		# Case 3: RL Team Scores
		if RLTeamScored:
			sim.scenic_reward += 1

		# Case 4: RL Agent Team takes a shot but misses: +0.5
		if not opTeamScored and ball.position.x >=100 and abs(ball.position.y) < 10:
			sim.scenic_reward += 0.5

		# Case 5: If RL Agent Team never takes possession of the ball by the end of the simulation, -0.5
		if rlTeamTakesPossession():
			RLTeamTakesPossession = True
		if sim.done and not RLTeamTakesPossession:
			sim.scenic_reward += -0.5

		# Case 6: If RL Team did not concede a goal in defense by the end of the simulation: +0.5
		if sim.done and not OpTeamScoresAtLeastOnce:
			sim.scenic_reward += 0.5

		prev_RLTeamScore = gameds.game_state.score[0]
		prev_opTeamScore = gameds.game_state.score[1]
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