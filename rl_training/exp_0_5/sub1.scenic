from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 70 @ 28

MyGK at -99 @ 0
MyCB at 70 @ 0
MyCB at 70 @ 30

OpGK at 99 @ 0
#OpCB at 75 @ 30