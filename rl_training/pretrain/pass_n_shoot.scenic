from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
# from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# ball at top
ball = Ball at 70 @ 28
ego = MyGK at -99 @ 0
gk = ego
# P2 Turing
p2 = MyCF at 70 @ 0
# P1 top with ball
p1 = MyCB at 70 @ 30
OpGK at 99 @ 0
OpCB at 75 @ 30