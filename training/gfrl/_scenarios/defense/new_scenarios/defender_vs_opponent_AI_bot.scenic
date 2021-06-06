from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle

param game_duration = 400
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

LeftGK at 95 @ 40, with HoldPosition()
left_defender = LeftRB

RightGK at 98 @ 40, with HoldPosition()
ego = RightAM on LeftReg_CM

Ball ahead of ego by 2