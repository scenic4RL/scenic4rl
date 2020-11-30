from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False

reg = RectangularRegion( 0 @ 0, 0, 10, 10)

ego = Ball in reg
mygk = MyPlayer on reg,
        with role "GK"

opgk = OpPlayer in reg, with role "GK"


print(ego.position)
print(mygk.position)
print(opgk.position)


