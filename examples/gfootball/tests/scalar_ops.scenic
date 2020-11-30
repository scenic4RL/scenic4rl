from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
import math
from math import degrees
param game_duration = 400
param deterministic = False

ego = MyPlayer at 0 @ 0,
        facing 270 deg,
        with role "GK"

ball = Ball at 10@10


op1 = OpPlayer at 30@30,
        facing toward ball, #135deg?
        with role "GK"


print(ego.position, degrees(ego.heading))
print(ball.position, degrees(ball.heading))
print(op1.position, degrees(op1.heading))

print(relative heading of op1)
print(relative heading of ego from op1)

print()
print(distance to op1)
print(distance from op1 to ego)
print(distance from op1 to ball)


#print(op2.position, degrees(op2.heading))
