from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = LeftGoalMidPoint

spot = Center

Ball at spot offset by Uniform(-1,1)@Uniform(-1,1)

MyPlayer with role "GK", left of spot by 10

OpPlayer with role "GK", right of spot by 10
