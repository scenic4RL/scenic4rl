from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


ego = MyPlayer with role "GK"
#a1 = MyPlayer with role "CB", with behavior MoveInDirection(5)
a1 = MyPlayer with role "CB", with behavior MoveToPosition(0,0)


o0 = OpPlayer with role "GK"
o1 = OpPlayer with role "CB", with behavior MoveToPosition(0,0)

Ball