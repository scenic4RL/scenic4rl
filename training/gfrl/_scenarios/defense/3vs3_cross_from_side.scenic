from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
param game_duration = 400
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True

leftLeftBackRegion = get_reg_from_edges(-70, -60, 20, 15)
leftCenterBackRegion = get_reg_from_edges(-70, -65, 10, -10)
leftRightMidRegion = get_reg_from_edges(-70, -65, -10, -20)

rightRightMidRegion  = get_reg_from_edges(-55, -50, 20, 15)
rightCenterMidRegion = get_reg_from_edges(-65, -60, 0, 5)
rightLeftMidRegion   = get_reg_from_edges(-55, -50, -30, -35)

rightRM_AttackRegion = get_reg_from_edges(-80, -70, 5, -5)
rightAM_AttackRegion = get_reg_from_edges(-90, -85, -5, -10)
rightLM_AttackRegion = get_reg_from_edges(-80, -75, -25, -30)

behavior runToReceiveCrossAndShoot(destinationPoint):
	do MoveToPosition(destinationPoint)
	do HoldPosition() until self.owns_ball
	do dribbleToAndShoot(-80 @ 0)
	do HoldPosition()

behavior rightLMBehavior(destinationPoint):
	do MoveToPosition(destinationPoint)
	do HighPassTo(Uniform(ego, right_RightMid))
	do HoldPosition()

RightGK
right_RightMid = RightRM on rightRightMidRegion, with behavior runToReceiveCrossAndShoot(Point on rightRM_AttackRegion)
ego = RightAM on rightCenterMidRegion, with behavior runToReceiveCrossAndShoot(Point on rightAM_AttackRegion)
right_LeftMid = RightLM on rightLeftMidRegion, with behavior rightLMBehavior(Point on rightLM_AttackRegion)
ball = Ball ahead of right_LeftMid by 2

LeftGK with behavior HoldPosition()
leftLB = LeftLB on leftLeftBackRegion
leftCB = LeftCB on leftCenterBackRegion
leftRB = LeftRM on leftRightMidRegion

