from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
import math

param game_duration = 600
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ball = Ball at 0 @ 0,
        facing 90 deg
ego = ball

mp =  MyPlayer with role "GK", ahead of ball by 10 # should be at [-10, 0]
op1 = OpPlayer with role "GK", behind ball by 10   # should be at [10, 0]


print("Ball: ", ball.position, math.degrees(ball.heading))
print(f"My Player: ", mp.position, math.degrees(mp.heading))
print(f"Op Player: ", op1.position, math.degrees(op1.heading))