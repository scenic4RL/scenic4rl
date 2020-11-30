from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = LeftGoalMidPoint

b = Ball
MyPlayer with role "GK", left of b by 10
OpPlayer with role "GK", right of b by 10
