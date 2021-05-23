from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1

MyCenterBackRegion = get_reg_from_edges(-70, -60, 10, -10)
MyLeftBackRegion = get_reg_from_edges(-10, 0, 30, 20)
MyRightBackRegion = get_reg_from_edges(-10, 0, -20, -30)

OpCenterMidRegion = get_reg_from_edges(-50, -40, 5, -5)
OpLeftMidRegion = get_reg_from_edges(-60, -50, -20, -30)

MyGK at 95 @ 40, with behavior IdleBehavior()
myLB = MyLB on MyLeftBackRegion
myCB = MyCB on MyCenterBackRegion
myRB = MyRM on MyRightBackRegion

OpGK at 95 @ 40, with behavior IdleBehavior()
ego = OpCM on OpCenterMidRegion
opCM = OpLM on OpLeftMidRegion

Ball ahead of ego by 0.5