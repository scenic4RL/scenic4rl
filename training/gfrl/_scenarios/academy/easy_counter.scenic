from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 26 @ 11

LeftGK at -99 @ 0
LeftLB at -67.2 @  19.576
LeftCB at -75  @    6.356
LeftCB at -75  @  -6.3559
LeftRB at -67.2 @ -19.576
LeftCM at -43.4 @  10.568
LeftCM at -43.4 @ -10.568
LeftCM at  50 @ 31.61
LeftLM at  25 @ 10
LeftRM at  25 @ -10
LeftCF at  35 @ -31.6102


RightGK at 99 @ 0
RightLB at -12.8 @ -19.576
RightCB at  -40 @ -6.356
RightCB at   40 @ 6.3559
RightRB at -12.8 @ -19.576
RightCM at -36.5 @ -10.568
RightCM at -28.2 @ 0
RightCM at -36.5 @ 10.568
RightLM at -54 @ -31.61
RightRM at -51 @ 0.0
RightCF at -54 @ 31.6102
