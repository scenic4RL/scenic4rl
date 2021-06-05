from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 70 @ 28

dx = 5
dy = 5

MyGK at -99 @ 0
MyCB in get_reg_from_edges(70-dx, 70+dx, 0-dy, 0+dy)#at 70 @ 0
MyCB in get_reg_from_edges(70-dx, 70+dx, 30-dy, 30+dy)#at 70 @ 30

OpGK at 99 @ 0
OpCB in get_reg_from_edges(75-dx, 75+dx, 10-dy, 10+dy)#at 75 @ 10