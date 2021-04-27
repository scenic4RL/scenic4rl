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

MyLB at -60 @  30
MyCB at -70 @  12
MyCB at -70 @ -12
MyRB at -60 @ -30

MyLM at -25 @  15
MyCM at -50 @  10
MyCM at -50 @ -10
MyRM at -25 @ -15

MyAM at -15 @ -2

MyCF at  -2 @ -1

OpGK
