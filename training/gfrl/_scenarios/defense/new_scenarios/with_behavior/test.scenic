from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

rightRM_AttackRegion = get_reg_from_edges(-80, -70, 10, 5)

LeftGK at 95 @ 40, with behavior HoldPosition()
# LeftGK with behavior HoldPosition()
left_defender1 = LeftCB 
left_defender2 = LeftCB 

behavior GiveAndGo():
	try:
		do ShortPassTo(right_attacking_midfielder)
		do MoveToPosition(-80 @ 0)
	interrupt when self.owns_ball and left_penaltyBox.containsPoint(self.position):
		do AimGoalCornerAndShoot()
	interrupt when self.owns_ball 

RightGK at 95 @ 40, with behavior HoldPosition()
# RightGK with behavior HoldPosition()
ego = RightCM on LeftReg_CM
right_attacking_midfielder = RightAM on LeftReg_CM

Ball ahead of ego by 2

require (distance from left_defender1 to left_defender2) > 3
require (distance from ego to right_attacking_midfielder) > 4