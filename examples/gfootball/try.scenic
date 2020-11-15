from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = LeftGoalMidPoint

MyPlayer with role "GK", in pbox_left

OpPlayer with role "GK",
         in pbox_left

Ball in pbox_left
