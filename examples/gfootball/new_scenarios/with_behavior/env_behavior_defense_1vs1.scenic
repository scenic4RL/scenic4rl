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


behavior egoBehavior(destination_point):
	try:
		do dribbleToAndShoot(destination_point)
	interrupt when (distance from self to ball) > 2:
		do FollowObject(ball, sprint=True)
	do IdleBehavior()

defender_region = get_reg_from_edges(-52, -48, 5, -5)
attacker_region = get_reg_from_edges(-26, -22, 5, -5)

YellowGK with behavior HoldPosition()
yellow_defender = YellowCB

BlueGK
ego = BlueCM on attacker_region, with behavior egoBehavior(-80 @ 0)
ball = Ball ahead of ego by 2

# yellow_defender = YellowCB on yellow_penaltyBox
# YellowGK on yellow_penaltyBox
# BlueGK on yellow_penaltyBox
# ego = BlueCM on yellow_penaltyBox
# Ball ahead of ego by 2
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
# BlueCM on yellow_penaltyBox
