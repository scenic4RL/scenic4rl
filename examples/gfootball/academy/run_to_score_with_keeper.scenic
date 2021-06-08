from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


# -----SET UP-----
Ball at 2 @ 0
# Left Team
ego = LeftGK at -99 @ 0
p1 = LeftCB at 0 @ 0
# Right Team
RightGK at 99 @ 0
RightLB at -12 @ 20
RightCB at -12 @ 10
RightCM at -12 @ 0
RightCB at -12 @ -10
RightRB at -12 @ -20
