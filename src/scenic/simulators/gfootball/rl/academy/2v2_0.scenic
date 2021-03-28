from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import BuiltinAIBot, IdleBehavior, JustShoot, JustPass

param game_duration = 50
param deterministic = True
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 67 @ 6

MyGK at -99 @ 0
MyCF at 92 @ -2
MyAM at 65 @ 8

OpGK at 99.5 @ 4
OpRB at -65 @ -5


#builtin ai 5 out of 5, random 0/5
#random performance 11/100  [mean 0.11 out of 100 trials]