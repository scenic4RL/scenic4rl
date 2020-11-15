from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = LeftGoalMidPoint

MyPlayer with role "GK",
         offset by 5 @ -10

OpPlayer with role "GK",
         at -85 @ -24

Ball offset by 10 @ -20
