from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *


num_player = 2
param game_duration = 600
param deterministic = False
param players = ['agent:left_players=3', "keyboard:right_players=1"]

#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = Ball at 0 @ 0

mygk = MyGK with behavior GreedyPlay()

MyLB with behavior GreedyPlay(), at 5@5
MyCB with behavior GreedyPlay(), at -5@6
MyRB with behavior GreedyPlay(), at 10@10

OpPlayer with role "GK", in right_pbox
