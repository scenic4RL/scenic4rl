from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True
param render = False

ego = Ball at 70 @ 28

MyGK at -98 @ 0
MyAM at 70 @ 0
MyCF at 70 @ 30

OpGK at 98 @ 0
OpCB at 75 @ 10