from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 52 @ 0

LeftGK at -98 @  0
LeftAM at 50 @  0
LeftCF at 80 @ -10

RightGK at  98 @   0
RightCB at  70 @  -5

