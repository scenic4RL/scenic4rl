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

LeftGK at -98 @  0
LeftAM in get_reg_from_edges(75+dx, 75-dx, -15+dx, -15-dx)
LeftCF in get_reg_from_edges(75+dx, 75-dx, 15+dx, 15-dx)

RightGK at 98 @ 0
RightCB in get_reg_from_edges(75+dx, 75-dx, dx, -dx)

