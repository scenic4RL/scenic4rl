from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 50
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 90 @ 0

MyGK at -99 @ 0
MyCF at 92 @ -2
MyAM at 65 @ 8

OpGK at 99.5 @ 4
OpRB at 65 @ -5

#builtin ai 100 out of 100,
#random performance  6/100  [mean  0.06 out of 100 trials]