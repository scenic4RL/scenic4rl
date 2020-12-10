from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 200
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

mygk = MyGK


MyLB
MyCB
MyRB

MyDM
MyLM
MyCM
MyRM

MyAM
MyCF

ego = mygk

OpPlayer with role "GK",
         in right_pbox

Ball at 0 @ 0