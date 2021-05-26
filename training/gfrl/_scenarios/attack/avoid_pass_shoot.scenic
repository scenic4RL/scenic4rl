from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 52 @ 0

YellowGK at -98 @  0
YellowAM at 50 @  0
YellowCF at 80 @ -10

BlueGK at  98 @   0
BlueCB at  70 @  -5

