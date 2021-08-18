from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 62 @ 0

LeftGK at -99 @ 0
LeftCM at 60 @ 0
LeftCM at 70 @ 20
LeftCM at 70 @ -20


RightGK at 99 @ 0
RightCB at 75 @ 0