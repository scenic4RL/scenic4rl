from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from math import degrees

param game_duration = 400
param deterministic = True


ego = MyPlayer at -90@0,
        facing toward center,
        with role "GK"

ball = Ball in right_pbox

OpPlayer at 90@0, with role "GK"

grid_len = 5
g00 = grid(0,0, grid_len)
gtr = grid(2, 2, grid_len)
gbr = grid(2, -2, grid_len)
gtl = grid(-2, 2, grid_len)
gbl  = grid(-2, -2, grid_len)
g1m0p = grid(-1, 0, grid_len)

print(ego.position, degrees(ego.heading))
print(g00.position, g00.corners, g00.length, g00.width)
print(gtr.position, gtr.corners, gtr.length, gtr.width)
print(gbr.position, gbr.corners, gbr.length, gbr.width)
print(gtl.position, gtl.corners, gtl.length, gtl.width)
print(gbl.position, gbl.corners, gbl.length, gbl.width)
print(g1m0p.position, g1m0p.corners, g1m0p.length, g1m0p.width)

"""
Expected
(0.0 @ 0.0) ((20.0 @ 8.4), (-20.0 @ 8.4), (-20.0 @ -8.4), (20.0 @ -8.4)) 16.8 40.0
(80.0 @ 33.6) ((100.0 @ 42.0), (60.0 @ 42.0), (60.0 @ 25.2), (100.0 @ 25.2)) 16.8 40.0
(80.0 @ -33.6) ((100.0 @ -25.2), (60.0 @ -25.2), (60.0 @ -42.0), (100.0 @ -42.0)) 16.8 40.0
(-80.0 @ 33.6) ((-60.0 @ 42.0), (-100.0 @ 42.0), (-100.0 @ 25.2), (-60.0 @ 25.2)) 16.8 40.0
(-80.0 @ -33.6) ((-60.0 @ -25.2), (-100.0 @ -25.2), (-100.0 @ -42.0), (-60.0 @ -42.0)) 16.8 40.0
(-40.0 @ 0.0) ((-20.0 @ 8.4), (-60.0 @ 8.4), (-60.0 @ -8.4), (-20.0 @ -8.4)) 16.8 40.0
"""