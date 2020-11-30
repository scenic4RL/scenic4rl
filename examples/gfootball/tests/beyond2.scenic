from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from math import degrees
import math
param game_duration = 400
param deterministic = False

ego = MyPlayer at 0 @ 0,
        facing 0 deg,
        with role "GK"

ball = Ball at 10 @ 0

op1 = OpPlayer beyond ball by (10 @ 10),
        with role "GK"  # should be placed at (20,-10)

print(ego.position, degrees(ego.heading))
print(ball.position, degrees(ball.heading))
print(op1.position, degrees(op1.heading))


