from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 52 @ 18

MyGK at -98 @  0
MyAM at 50 @  20
MyCF at 80 @ -10

OpGK at  98 @  0
OpCB at  60 @ 20

