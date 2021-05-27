from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

dx = 2
ego = Ball at 77 @ -13

YellowGK at -98 @  0
YellowAM in get_reg_from_edges(75+dx, 75-dx, -15+dx, -15-dx)
YellowCF in get_reg_from_edges(75+dx, 75-dx, 15+dx, 15-dx)

BlueGK at 98 @ 0
BlueCB in get_reg_from_edges(75+dx, 75-dx, dx, -dx)

