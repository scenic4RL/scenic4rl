from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

leftCBInitialRegion = get_reg_from_edges(65, 70, -25, -35)
rightCBInitialRegion  = get_reg_from_edges(75, 80, -20, -30)

LeftGK at -99 @ 0
LeftCB at 70 @ 0
ego = LeftCB on leftCBInitialRegion

RightGK at 99 @ 0
RightCB on rightCBInitialRegion

Ball ahead of ego by 2