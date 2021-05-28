from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

leftLeftBackRegion = get_reg_from_edges(-70, -60, 20, 15)
leftCenterBackRegion = get_reg_from_edges(-70, -65, 10, -10)
leftRightBackRegion = get_reg_from_edges(-70, -65, -20, -25)

rightRightMidRegion  = get_reg_from_edges(-55, -50, 20, 15)
rightCenterMidRegion = get_reg_from_edges(-55, -50, -10, -20)
rightLeftMidRegion   = get_reg_from_edges(-55, -50, -30, -40)

# LeftGK at 95 @ 40, with behavior HoldPosition()
LeftGK with behavior HoldPosition()
leftLB = LeftLB on leftLeftBackRegion
leftCB = LeftCB on leftCenterBackRegion
leftRB = LeftRM on leftRightBackRegion

# RightGK at 98 @ 40, with behavior HoldPosition()
RightGK with behavior HoldPosition()
opRM = RightRM on rightRightMidRegion
opAM = RightAM on rightCenterMidRegion
ego = RightLM on rightLeftMidRegion

Ball ahead of ego by 0.5


