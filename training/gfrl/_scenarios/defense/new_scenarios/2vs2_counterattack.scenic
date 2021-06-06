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

LeftMidRegion = get_reg_from_edges(-1, 5, 35, 30)
egoInitialRegion  = get_reg_from_edges(-40, -35, 5, -5)
egoAttackRegion = get_reg_from_edges(-80, -75, 5, 0)
rightRMAttackRegion = get_reg_from_edges(-80, -75, 5, -5)

LeftGK at 95 @ 40, with behavior HoldPosition()
left_defender1 = LeftRB
left_defender2 = LeftLM on LeftMidRegion

RightGK at 98 @ 40, with behavior HoldPosition()

rightRM = RightRM
ego = RightAM on egoInitialRegion

ball = Ball ahead of rightRM by 2