from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

#1500 is 45 minutes
param game_duration = 1000
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

mygk = MyGK with behavior GreedyPlay()

MyLB with behavior GreedyPlay()
MyCB with behavior GreedyPlay()
MyRB with behavior GreedyPlay()

MyDM with behavior GreedyPlay()
MyLM with behavior GreedyPlay()
MyCM with behavior GreedyPlay()
MyRM with behavior GreedyPlay()

MyAM with behavior GreedyPlay()
MyCF with behavior GreedyPlay()

ego = mygk

OpPlayer with role "GK",
         in right_pbox

Ball at 0 @ 0