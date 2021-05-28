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

MyLeftMidRegion = get_reg_from_edges(-1, 5, 35, 30)
egoInitialRegion  = get_reg_from_edges(-40, -35, 5, -5)
egoAttackRegion = get_reg_from_edges(-80, -75, 5, 0)
rightRMAttackRegion = get_reg_from_edges(-80, -75, 5, -5)
fallBackRegion = get_reg_from_edges(-70, -60, 5, -5)

# LeftGK with behavior HoldPosition()
LeftGK at 95 @ 40, with behavior HoldPosition()
left_defender1 = LeftRB
left_defender2 = LeftLM on MyLeftMidRegion

# RightGK
RightGK at 98 @ 40, with behavior HoldPosition()
ego_destinationPoint = Point on egoAttackRegion
rightRM_destinationPoint = Point on rightRMAttackRegion

rightRM = RightRM
ego = RightAM on egoInitialRegion

ball = Ball ahead of rightRM by 0.1