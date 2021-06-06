from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
param game_duration = 12
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True

leftLeftBackRegion = get_reg_from_edges(-70, -65, 5, -5)
leftCenterBackRegion = get_reg_from_edges(-70, -65, 5, -5)
leftRightBackRegion = get_reg_from_edges(-70, -65, 5, -5)

rightRightMidRegion  = get_reg_from_edges(-70, -65, 5, -5)
rightCenterMidRegion = get_reg_from_edges(-70, -65, 5, -5)
rightLeftMidRegion   = get_reg_from_edges(-70, -65, 5, -5)

rightRM_AttackRegion = get_reg_from_edges(-70, -65, 5, -5)
rightAM_AttackRegion = get_reg_from_edges(-70, -65, 5, -5)
rightLM_AttackRegion = get_reg_from_edges(-70, -65, 5, -5)

behavior runToReceiveCrossAndShoot(destinationPoint):
	do MoveToPosition(destinationPoint)
	do HoldPosition() until self.owns_ball
	do dribbleToAndShoot(-80 @ 0)
	do HoldPosition()

behavior rightLMBehavior():
	destinationPoint = Point on rightLM_AttackRegion
	do MoveToPosition(destinationPoint)
	do HighPassTo(Uniform(ego, right_RightMid))
	do HoldPosition()

RightGK
right_RightMid = RightRM on rightRightMidRegion, with behavior runToReceiveCrossAndShoot(Point on rightRM_AttackRegion)
ego = RightAM on rightCenterMidRegion, with behavior runToReceiveCrossAndShoot(Point on rightAM_AttackRegion)
right_LeftMid = RightLM on rightLeftMidRegion, with behavior rightLMBehavior()
ball = Ball ahead of right_LeftMid by 2

LeftGK with behavior HoldPosition()
leftLB = LeftLB on leftLeftBackRegion
leftCB = LeftCB on leftCenterBackRegion
leftRB = LeftRM on leftRightBackRegion

