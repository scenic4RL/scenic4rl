from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from math import degrees
param game_duration = 400
param deterministic = False

ego = MyPlayer with role "GK"
ball = Ball


print(right_goal.position, right_goal.corners, right_goal.length, right_goal.width)
#Expected: (99.95 @ 0) ((100.0 @ 4.4), (99.9 @ 4.4), (99.9 @ -4.4), (100.0 @ -4.4)) 8.8 0.1, when width 0.1 and height 8.8

print(left_goal.position, left_goal.corners, left_goal.length, left_goal.width)
#Expected: (-99.95 @ 0) ((-99.9 @ 4.4), (-100.0 @ 4.4), (-100.0 @ -4.4), (-99.9 @ -4.4)) 8.8 0.1, , when width 0.1 and height 8.8

