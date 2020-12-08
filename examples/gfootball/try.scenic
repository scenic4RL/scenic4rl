from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 100
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = Ball at 0 @ 0

MyPlayer with role "GK", in left_pbox

OpPlayer with role "GK",
         in left_pbox


