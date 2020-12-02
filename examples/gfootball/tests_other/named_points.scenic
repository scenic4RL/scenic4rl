from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from math import degrees

param game_duration = 400
param deterministic = True


ego = MyPlayer at -90@0,
        facing toward center,
        with role "GK"

ball = Ball at (corner_tr.x-2)@(corner_tr.y-2)

OpPlayer at 90@0, with role "GK"

print(center)
print(corner_tl)
print(corner_tr)
print(corner_bl)
print(corner_br)

"""
Expected: 
(0 @ 0)
(-100.0 @ 42.0)
(100.0 @ 42.0)
(-100.0 @ -42.0)
(100.0 @ -42.0)
"""
