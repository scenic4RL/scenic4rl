from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 300
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = LeftGoalMidPoint

MyPlayer with role "GK",
         offset along 45 deg by 40 @ 0
         #offset along 45 deg by 25 @ 10

OpPlayer with role "GK",
         offset along 25 deg by 51 @ 0

Ball offset along 89 deg by 41 @ 0