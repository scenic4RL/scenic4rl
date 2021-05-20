from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

MyLeftBackRegion = get_reg_from_edges(-70, -60, 20, 15)
MyCenterBackRegion = get_reg_from_edges(-70, -65, 10, -10)
MyRightBackRegion = get_reg_from_edges(-70, -65, -20, -25)

OpRightMidRegion  = get_reg_from_edges(-55, -50, 20, 15)
OpCenterMidRegion = get_reg_from_edges(-55, -50, -10, -20)
OpLeftMidRegion   = get_reg_from_edges(-55, -50, -30, -40)

MyGK at 95 @ 40
myLB = MyLB on MyLeftBackRegion
myCB = MyCB on MyCenterBackRegion
myRB = MyRM on MyRightBackRegion

OpGK at 95 @ 40
opRM = OpRM on OpRightMidRegion
opAM = OpAM on OpCenterMidRegion
ego = OpLM on OpLeftMidRegion

Ball ahead of ego by 1


