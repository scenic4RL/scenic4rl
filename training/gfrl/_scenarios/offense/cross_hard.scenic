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

LeftGK at -98 @  0
ego = LeftAM in get_reg_from_edges(x+10+dx, x+10-dx, -35+dx, -35-dx), facing -90 deg
Ball ahead of ego by 2
LeftCF in get_reg_from_edges(x+dx, x-dx, 6+dx, 6-dx)
LeftCF in get_reg_from_edges(x+dx, x-dx, -6+dx, -6-dx)

RightGK at 98 @ 0
RightCB in get_reg_from_edges(x+dx, x-dx, 12+dx, 12-dx)
RightCB in get_reg_from_edges(x+dx, x-dx, dx, -dx)
RightCB in get_reg_from_edges(x+dx, x-dx, -12+dx, -12-dx)

