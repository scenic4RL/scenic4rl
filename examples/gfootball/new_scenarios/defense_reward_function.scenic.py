
## I'm assuming that simulation().reward is always instantiated as 0

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

	while True:
		RLTeamScored = prev_RLTeamScore + 1 == gameds.game_state.score[0]
		opTeamScored = prev_opTeamScore + 1 == gameds.game_state.score[1]

		# Case 1: Opponent Team Scores
		if opTeamScored:
			sim.scenic_reward += -1
			OpTeamScoresAtLeastOnce = True

		# Case 2: Opponent Team takes a shot but misses scoring: -0.5
		# I took out the condition about "once" because the simulation will terminate if the ball goes off the field
		if not RLTeamScored and ball.position.x <= -100 and abs(ball.position.y) < 10:
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