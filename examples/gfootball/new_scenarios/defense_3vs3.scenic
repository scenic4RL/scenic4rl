from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1

MyLeftBackRegion = get_reg_from_edges(-70, -60, 20, 15)
MyCenterBackRegion = get_reg_from_edges(-70, -65, 10, -10)
MyRightBackRegion = get_reg_from_edges(-70, -65, -20, -25)

OpRightMidRegion  = get_reg_from_edges(-55, -50, 20, 15)
OpCenterMidRegion = get_reg_from_edges(-55, -50, -10, -20)
OpLeftMidRegion   = get_reg_from_edges(-55, -50, -30, -40)

MyGK at 95 @ 40, with behavior IdleBehavior()
myLB = MyLB on MyLeftBackRegion
myCB = MyCB on MyCenterBackRegion
myRB = MyRM on MyRightBackRegion

OpGK at 95 @ 40, with behavior IdleBehavior()
opRM = OpRM on OpRightMidRegion
opAM = OpAM on OpCenterMidRegion
ego = OpLM on OpLeftMidRegion

Ball ahead of ego by 0.5


