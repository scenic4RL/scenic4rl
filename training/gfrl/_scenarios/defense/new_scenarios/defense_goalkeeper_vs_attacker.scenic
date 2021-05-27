from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1

MyGK
OpGK at 95 @ 40, with behavior IdleBehavior()
ego = OpAM on LeftReg_CM

Ball ahead of ego by 0.5