from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 62 @ 0

YellowGK at -99 @ 0
YellowCM at 60 @ 0
YellowCM at 70 @ 20
YellowCM at 70 @ -20


BlueGK at 99 @ 0
BlueCB at 75 @ 0