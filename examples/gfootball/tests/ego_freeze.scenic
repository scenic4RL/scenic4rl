from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
a0 = MyGK
ego = MyLB
#ego = MyGK

o0 = OpGK
Ball