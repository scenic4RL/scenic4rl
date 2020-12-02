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

print(left_pbox.position, left_pbox.corners, left_pbox.length, left_pbox.width)
#Expected: (-85.5 @ 0) ((-71.0 @ 24.0), (-100.0 @ 24.0), (-100.0 @ -24.0), (-71.0 @ -24.0)) 48 29 #width 28 and height 48
print(right_pbox.position, right_pbox.corners, right_pbox.length, right_pbox.width)
#Expected: (85.5 @ 0) ((71 @ -24), (100. @ -24), (100 @ 24), (71 @ 24)) 48 29

print(center) #0@0

