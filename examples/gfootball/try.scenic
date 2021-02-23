from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 50
param deterministic = False

ego = MyGK in left_pbox
MyLB in right_pbox
MyRB in right_pbox
MyCF in right_pbox
#o0 = OpGK in right_pbox
ball = Ball in right_pbox

