from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *


param manual_control = False
param game_duration = 200
param deterministic = False
param real_time = False
param dump_full_episodes = True
param dump_scores = True
param write_video = True

#how to specify that if there is one/ more than one player on one side, there must be one GK??

Ball at 0 @ 0

ego = MyGK with behavior GreedyPlay(), at -90 @ 10
MyCB with behavior GreedyPlay(), at -50 @ 0
MyCF with behavior GreedyPlay(), at -10 @ 0

OpGK with behavior BuiltinAIBot(), at 90 @ 10
OpCF with behavior BuiltinAIBot(), at 10 @ 0


