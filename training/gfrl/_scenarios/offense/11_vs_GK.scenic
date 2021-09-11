from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 0 @ 0

LeftGK at -98 @ 0

LeftLB at -60 @  30
LeftCB at -70 @  12
LeftCB at -70 @ -12
LeftRB at -60 @ -30

LeftLM at -25 @  15
LeftCM at -50 @  10
LeftCM at -50 @ -10
LeftRM at -25 @ -15
LeftAM at -15 @ -2

LeftCF at  -2 @ -1

RightGK
