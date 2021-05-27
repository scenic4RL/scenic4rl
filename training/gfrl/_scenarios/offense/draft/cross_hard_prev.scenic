from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

dx = 2

x = 70

YellowGK at -98 @  0
ego = YellowAM in get_reg_from_edges(x+10+dx, x+10-dx, -35+dx, -35-dx), facing -90 deg
Ball ahead of ego by 2
YellowCF in get_reg_from_edges(x+dx, x-dx, 10+dx, 10-dx)
YellowCF in get_reg_from_edges(x+dx, x-dx, -10+dx, -10-dx)

BlueGK at 98 @ 0
BlueCB in get_reg_from_edges(x+dx, x-dx, 20+dx, 20-dx)
BlueCB in get_reg_from_edges(x+dx, x-dx, dx, -dx)
BlueCB in get_reg_from_edges(x+dx, x-dx, -20+dx, -20-dx)

