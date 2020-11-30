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
        apparently facing 0 deg,
        with role "GK"

op2 = OpPlayer at 30@-30,
        apparently facing 0 deg

op3 = OpPlayer at 40@-40,
        apparently facing 10 deg

print(ego.position, degrees(ego.heading))
print(op1.position, degrees(op1.heading))
print(op2.position, degrees(op2.heading))
print(op3.position, degrees(op3.heading))