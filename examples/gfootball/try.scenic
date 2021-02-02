from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 100
param deterministic = False
param render = True

#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = Ball at 0 @ 0

MyGK
MyCM
MyCM

OpGK
OpCM
OpCM

