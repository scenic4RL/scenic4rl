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

leftLeftBackRegion = get_reg_from_edges(-70, -60, 20, 15)
leftCenterBackRegion = get_reg_from_edges(-70, -65, 10, -10)
leftRightMidRegion = get_reg_from_edges(-70, -65, 25, 20)

rightRightMidRegion  = get_reg_from_edges(-55, -50, 20, 15)
rightCenterMidRegion = get_reg_from_edges(-55, -50, -10, -20)
rightLeftMidRegion   = get_reg_from_edges(-55, -50, 40, 30)

LeftGK at 95 @ 40, with behavior HoldPosition()
leftLB = LeftLB on leftLeftBackRegion
leftCB = LeftCB on leftCenterBackRegion
leftRB = LeftRB on leftRightMidRegion

RightGK at 98 @ 40, with behavior HoldPosition()
opRM = RightRM on rightRightMidRegion
opAM = RightAM on rightCenterMidRegion
ego = RightLM on rightLeftMidRegion

Ball ahead of ego by 2


