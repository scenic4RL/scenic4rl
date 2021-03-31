from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ball = Ball at 2 @ 0
ego = ball

MyGK at -98 @ 0, with behavior RunThenShoot()
MyCB at 0 @ 0, with behavior RunThenShoot()


OpGK at -98 @ -41
OpLB at -22 @ -20
OpCB at -22 @ -10
OpCM at -22 @ 0
OpCB at -22 @ 10
OpRB at -22 @ 20