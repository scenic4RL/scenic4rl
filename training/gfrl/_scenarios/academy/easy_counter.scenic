from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 26 @ 11

MyGK at -99 @ 0
MyLB at -67.2 @  19.576
MyCB at -75  @    6.356
MyCB at -75  @  -6.3559
MyRB at -67.2 @ -19.576
MyCM at -43.4 @  10.568
MyCM at -43.4 @ -10.568
MyCM at  50 @ 31.61
MyLM at  25 @ 10
MyRM at  25 @ -10
MyCF at  35 @ -31.6102


OpGK at 99 @ 0
OpLB at -12.8 @ -19.576
OpCB at  -40 @ -6.356
OpCB at   40 @ 6.3559
OpRB at -12.8 @ -19.576
OpCM at -36.5 @ -10.568
OpCM at -28.2 @ 0
OpCM at -36.5 @ 10.568
OpLM at -54 @ -31.61
OpRM at -51 @ 0.0
OpCF at -54 @ 31.6102
