from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle
import pdb

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

behavior egoBehavior(player, destinationPoint):
		do Uniform(ShortPassTo(player), dribbleToAndShoot(destinationPoint))

behavior attackMidBehavior()
	try:
		do HoldPosition()
	interrupt when self.ball_possession is True:
		do AimGoalCornerAndShoot()
	interrupt when (distance to nearestOpponentPlayer(self)) < 5:
		do dribble_evasive_zigzag()

YellowGK
yellow_attack_midfielder = YellowAM on blueTeam_penalty_arc_region, 
								facing north,
								with behavior attackMidBehavior()
ego = YellowLM ahead of yellow_attack_midfielder by Range(5, 10), 
		facing toward yellow_attack_midfielder,
		with behavior egoBehavior(yellow_attack_midfielder, yellow_penaltyBox_center)
Ball ahead of ego by 0.1

BlueRB left of ego by Range(3,5)
BlueGK


