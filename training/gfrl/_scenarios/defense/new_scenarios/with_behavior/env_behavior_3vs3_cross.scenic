# from scenic.simulators.gfootball.model import *
# from scenic.simulators.gfootball.behaviors import *
# from scenic.simulators.gfootball.simulator import GFootBallSimulator

# param game_duration = 400
# param deterministic = False
# param offsides = False
# param right_team_difficulty = 1
# param end_episode_on_score = True
# param end_episode_on_out_of_play = True
# # param end_episode_on_possession_change = True

# leftLeftBackRegion = get_reg_from_edges(-70, -60, 20, 15)
# leftCenterBackRegion = get_reg_from_edges(-70, -65, 10, -10)
# leftRightBackRegion = get_reg_from_edges(-70, -65, -20, -25)

# rightRightMidRegion  = get_reg_from_edges(-55, -50, 20, 15)
# rightCenterMidRegion = get_reg_from_edges(-55, -50, -10, -20)
# rightLeftMidRegion   = get_reg_from_edges(-55, -50, -30, -35)

# rightRM_AttackRegion = get_reg_from_edges(-80, -70, 10, 5)
# rightAM_AttackRegion = get_reg_from_edges(-80, -70, 5, -5)

# behavior rightRMBehavior():
# 	destinationPoint = Point on rightRM_AttackRegion
# 	do MoveToPosition(destinationPoint)
# 	do IdleBehavior()

# behavior rightAMBehavior():
# 	destinationPoint = Point on rightAM_AttackRegion
# 	do MoveToPosition(destinationPoint)
# 	do IdleBehavior()

# behavior egoBehavior():
# 	destinationPoint = Point at -80 @ -35
# 	do MoveToPosition(destinationPoint)
# 	do IdleBehavior()

# LeftGK
# leftLB = LeftLB on leftLeftBackRegion
# leftCB = LeftCB on leftCenterBackRegion
# leftRB = LeftRM on leftRightBackRegion

# RightGK
# ego = RightLM at -80 @ -35, with behavior egoBehavior()
# right_RightMid = RightRM with behavior rightRMBehavior()
# right_AttackingMid = RightAM with behavior rightAMBehavior()

# Ball ahead of ego by 2

from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
param game_duration = 400
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
# param end_episode_on_possession_change = True

leftLeftBackRegion = get_reg_from_edges(-70, -60, 20, 15)
leftCenterBackRegion = get_reg_from_edges(-70, -65, 10, -10)
leftRightBackRegion = get_reg_from_edges(-70, -65, -20, -25)

rightRightMidRegion  = get_reg_from_edges(-55, -50, 20, 15)
rightCenterMidRegion = get_reg_from_edges(-65, -60, 0, 5)
rightLeftMidRegion   = get_reg_from_edges(-55, -50, -30, -35)

rightRM_AttackRegion = get_reg_from_edges(-80, -70, 10, 5)
rightAM_AttackRegion = get_reg_from_edges(-80, -70, 5, 0)

behavior rightRMBehavior():
	destinationPoint = -80 @ -30
	do MoveToPosition(destinationPoint)
	do IdleBehavior()

behavior rightAMBehavior():
	destinationPoint = Point on rightAM_AttackRegion
	do MoveToPosition(destinationPoint)
	do IdleBehavior()

behavior rightLMBehavior():
	destinationPoint = -80 @ 30
	do MoveToPosition(destinationPoint)
	do HighPassTo(ego)
	do IdleBehavior()

RightGK
right_LeftMid = RightLM on rightLeftMidRegion, with behavior rightLMBehavior()
right_RightMid = RightRM on rightRightMidRegion, with behavior rightRMBehavior()
ego = RightAM on rightCenterMidRegion, with behavior rightAMBehavior()
ball = Ball ahead of right_LeftMid by 2

LeftGK with behavior HoldPosition()
leftLB = LeftLB on leftLeftBackRegion, with behavior IdleBehavior()
leftCB = LeftCB on leftCenterBackRegion, with behavior IdleBehavior()
leftRB = LeftRM on leftRightBackRegion, with behavior IdleBehavior()

