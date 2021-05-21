from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

MyCenterBackRegion = get_reg_from_edges(-70, -60, 10, -10)
MyLeftBackRegion = get_reg_from_edges(-10, 0, 30, 20)
MyRightBackRegion = get_reg_from_edges(-10, 0, -20, -30)

OpCenterMidRegion = get_reg_from_edges(-50, -40, 5, -5)
OpLeftMidRegion = get_reg_from_edges(-60, -50, -20, -30)

MyGK at -98 @ 0, with behavior IdleBehavior()
myLB = MyLB on MyLeftBackRegion
myCB = MyCB on MyCenterBackRegion
myRB = MyRM on MyRightBackRegion

OpGK at 99 @ 0
ego = OpCF on OpCenterMidRegion, facing 90 deg
opLM = OpLM on OpLeftMidRegion

Ball ahead of ego by 2