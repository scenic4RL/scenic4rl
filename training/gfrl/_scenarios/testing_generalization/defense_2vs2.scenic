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

LeftGK at 90 @ 40, with behavior HoldPosition()
left_defender1 = LeftCB on left_penaltyBox
left_defender2 = LeftCB on left_penaltyBox

RightGK at 95 @ 40, with behavior HoldPosition()
ego = RightCM on left_half_field
right_attacking_midfielder = RightAM on left_half_field

Ball ahead of ego by 2

require (distance from left_defender1 to left_defender2) > 3
require (distance from ego to right_attacking_midfielder) < 10