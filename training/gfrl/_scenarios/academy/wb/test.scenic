from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# -----SET UP-----
ball = Ball at 2 @ 0

# Left Team
ego = YellowGK at -99 @ 0
p1 = YellowCB at 0 @ 0

# Right Team
opgk = BlueGK at 99 @ 0
BlueLB at -12 @ 20
BlueCB at -12 @ 10
BlueCM at -12 @ 0
BlueCB at -12 @ -10
BlueRB at -12 @ -20
