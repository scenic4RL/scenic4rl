from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle

param game_duration = 400
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# LeftGK at 95 @ 40, with HoldPosition()
# LeftGK with behavior HoldPosition()
LeftGK
left_defender = LeftRB

# RightGK at 98 @ 40, with HoldPosition()
# RightGK with behavior HoldPosition()
RightGK
ego = RightAM on LeftReg_CM

Ball ahead of ego by 2


def yellowTakesPossession():
    ''' this includes case when the player itself has the ball possession '''
    for p in simulation().objects:
        if not isinstance(p, Ball) and p.team == 'yellow' and p.owns_ball:
            return True
    return False

monitor reward_function:
	sim = simulation()
	gameds = sim.game_ds
	yellowTakesPossession = False
	OpTeamScoresAtLeastOnce = False

	while True:
		yellowScored = prev_yellowScore + 1 == gameds.game_state.score[0]
		opTeamScored = prev_opTeamScore + 1 == gameds.game_state.score[1]

		# Case 1: Blue Team Scores
		if opTeamScored:
			sim.scenic_reward += -1
			OpTeamScoresAtLeastOnce = True

		# Case 2: Blue Team takes a shot but misses scoring: -0.5
		# I took out the condition about "once" because the simulation will terminate if the ball goes off the field
		if not yellowScored and ball.position.x <= -100 and abs(ball.position.y) < 10:
			sim.scenic_reward += -0.5 

		# Case 3: RL Team Scores
		if yellowScored:
			sim.scenic_reward += 1

		# Case 4: RL Agent Team takes a shot but misses: +0.5
		if not opTeamScored and ball.position.x >=100 and abs(ball.position.y) < 10:
			sim.scenic_reward += 0.5

		# Case 5: If RL Agent Team never takes possession of the ball by the end of the simulation, -0.5
		if yellowTakesPossession():	
			yellowTakesPossession = True
		if sim.done and not yellowTakesPossession:
			sim.scenic_reward += -0.5

		# Case 6: If RL Team did not concede a goal in defense by the end of the simulation: +0.5
		if sim.done and not OpTeamScoresAtLeastOnce:
			sim.scenic_reward += 0.5

		prev_yellowScore = gameds.game_state.score[0]
		prev_opTeamScore = gameds.game_state.score[1]
		wait