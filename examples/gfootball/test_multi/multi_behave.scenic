from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *


param manual_control = True
param game_duration = 200
param deterministic = False
param real_time = False
param dump_full_episodes = True
param dump_scores = True
param write_video = True

#how to specify that if there is one/ more than one player on one side, there must be one GK??

Ball at 0 @ 0

ego = MyGK with behavior GreedyPlay()

MyLB with behavior GreedyPlay()
MyCB with behavior GreedyPlay()
MyRB with behavior GreedyPlay()

OpGK with behavior BuiltinAIBot()
OpLB #with behavior BuiltinAIBot()
OpCB #with behavior BuiltinAIBot()

