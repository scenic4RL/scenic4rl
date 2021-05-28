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

leftCenterBackRegion = get_reg_from_edges(-70, -60, 10, -10)
leftLeftBackRegion = get_reg_from_edges(-10, 0, 30, 20)
leftRightBackRegion = get_reg_from_edges(-10, 0, -20, -30)

rightCenterMidRegion = get_reg_from_edges(-50, -40, 5, -5)
rightLeftMidRegion = get_reg_from_edges(-60, -50, -20, -30)

# LeftGK at 95 @ 40, with behavior HoldPosition()
LeftGK with behavior HoldPosition()
leftLB = LeftLB on leftLeftBackRegion
leftCB = LeftCB on leftCenterBackRegion
leftRB = LeftRM on leftRightBackRegion

# RightGK at 98 @ 40, with behavior HoldPosition()
RightGK with behavior HoldPosition()
ego = RightCM on rightCenterMidRegion
opCM = RightLM on rightLeftMidRegion

Ball ahead of ego by 2