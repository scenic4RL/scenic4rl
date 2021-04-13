from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 42 @ 0

MyGK at -98 @ 0
MyCB at 40 @ 0


OpGK at 98 @ 0
OpLB at -12 @ -20
OpCB at -12 @ -10
OpCM at -12 @ 0
OpCB at -12 @ 10
OpRB at -12 @ 20