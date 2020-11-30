from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
import math
from math import degrees
param game_duration = 600
param deterministic = False

ego = MyPlayer at 0 @ 0
ball = Ball at 30@30
op1 = OpPlayer at 30@-30


print(degrees(angle to ball)) #-45 deg
print(degrees(angle to op1))  #225 deg/-135
print(degrees(angle from op1 to ball))  #0