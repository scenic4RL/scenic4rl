from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param manual_control = False
param game_duration = 200
param deterministic = False
param real_time = True
param dump_full_episodes = False
param dump_scores = False
param write_video = False

#how to specify that if there is one/ more than one player on one side, there must be one GK??

Ball at 0 @ 0

ego = MyGK with behavior RunRight(), at -90 @ 10
MyCB with behavior RunRight(), at -50 @ 0
MyCF with behavior RunRight(), at -10 @ 0

OpGK at 90 @ 10, with behavior BuiltinAIBot()
OpCF at 10 @ 5, with behavior BuiltinAIBot()



