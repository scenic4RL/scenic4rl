from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *


num_player = 2
param game_duration = 600
param deterministic = False
param players = ['agent:left_players=3', "keyboard:right_players=1"]

#how to specify that if there is one/ more than one player on one side, there must be one GK??

Ball at 0 @ 0

ego = MyGK with behavior GreedyPlay()

MyLB with behavior GreedyPlay()
MyCB with behavior GreedyPlay()
MyRB with behavior GreedyPlay()

OpGK with behavior GreedyPlay()
OpLB with behavior GreedyPlay()
OpCB with behavior GreedyPlay()
OpRB with behavior GreedyPlay()
