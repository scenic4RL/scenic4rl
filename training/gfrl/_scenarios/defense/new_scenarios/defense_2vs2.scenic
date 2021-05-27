from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1

MyGK at 90 @ 40, with behavior IdleBehavior()
yellow_defender1 = MyCB 
yellow_defender2 = MyCB 


OpGK at 95 @ 40, with behavior IdleBehavior()
ego = OpCM on LeftReg_CM
blue_attacking_midfielder = OpAM on LeftReg_CM

Ball ahead of ego by 0.5

require (distance from yellow_defender1 to yellow_defender2) > 3
require (distance from ego to blue_attacking_midfielder) > 4