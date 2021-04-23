from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 0 @ 0

MyGK at -98 @ 0
MyCF at   -2 @ 0
MyAM at -25 @  5



OpGK at  98 @ 0
OpCF at   10 @ 0
OpAM at  25 @  -5
