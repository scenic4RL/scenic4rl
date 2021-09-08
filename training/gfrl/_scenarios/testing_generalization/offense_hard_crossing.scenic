from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


LeftGK at -98 @  0
ego = LeftAM in get_reg_from_edges(82, 78, 37, 33), facing -90 deg
Ball ahead of ego by 2
LeftCF in get_reg_from_edges(72, 68, 8, 4)
LeftCF in get_reg_from_edges(72, 68, -4, -8)

RightGK at 98 @ 0
RightCB in get_reg_from_edges(72, 68, 14, 10)
RightCB in get_reg_from_edges(72, 68, 2, -2)
RightCB in get_reg_from_edges(72, 68, -10, -14)

