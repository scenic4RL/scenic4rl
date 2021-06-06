from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

left_AM_initialRegion = get_reg_from_edges(77, 73, -13, -17)
left_CF_initialRegion = get_reg_from_edges(77, 73, 17, 13)
right_CB_initialRegion = get_reg_from_edges(77, 73, 2, -2)

LeftGK
LeftAM on left_AM_initialRegion
ego = LeftCF on left_CF_initialRegion
Ball ahead of ego by 2

RightGK
RightCB on right_CB_initialRegion
