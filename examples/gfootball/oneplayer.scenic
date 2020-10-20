from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False

#AskEddie: What is the significance of ego

#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = MyPlayer with role "GK"
MyPlayer
MyPlayer

#AskEddie how to define constants
OpPlayer with role "GK"
OpPlayer
OpPlayer

Ball
