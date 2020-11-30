from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
import math

param game_duration = 600
param deterministic = False

ego = MyPlayer at -90 @ 0,
            facing 0 deg,
            with role "GK"

op1 = OpPlayer with role "GK",
        offset along 270 deg by 0 @ 20  #op1 should be at (-70, 0)

ball = Ball offset along (-45 deg relative to ego.heading) by math.sqrt(200) @ 0  #ball should be at (-80, 10)?? [currently at -80, -10]

print("My Player: ", ego.position, ego.heading)
print("Opposition1: ", op1.position, op1.heading)
print("Ball: ", ball.position, ball.heading)