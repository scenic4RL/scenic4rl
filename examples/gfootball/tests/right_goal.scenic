from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from math import degrees
param game_duration = 400
param deterministic = False


#ego = MyPlayer at 70@0,
#        with role "CM"


ego = MyPlayer at 70 @ 0,
        facing toward right_goal.position,
        with role "GK"

ball = Ball at 90 @ 0

print(ego.position, degrees(ego.heading))



"""
ego = MyPlayer at 70@0,
            facing toward right_goal.position,
            with role "CF"
print(ego.position, degrees(ego.heading))
print(right_goal.position, right_goal.corners, right_goal.length, right_goal.width)
print(dir(right_goal))
"""