from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


# -----SET UP-----
ball = Ball at 26 @ 11

# Left Team
ego = LeftGK at -99 @ 0
LeftLB at -67.2 @ 19.576
LeftCB at -75 @ 6.356
LeftCB at -75 @ -6.3559
LeftRB at -67.2 @ -19.576
LeftCM at -43.4 @ 10.568
LeftCM at -43.4 @ -10.568
p4 = LeftCM at 50 @ 31.61
# Player with ball at the beginning
p1 = LeftLM at 25 @ 10
# good candidate down
p2 = LeftRM at 25 @ -10
# good candidate top
p3 = LeftCF at 35 @ -31.61


# Right Team
opgk = RightGK at 99 @ 0
RightLB at -12 @ -19
RightCB at -40 @ -6.356
RightCB at 40 @ 6.3559
RightRB at -13.5 @ -20.5
RightCM at -36.5 @ -10.568
RightCM at -28.2 @ 0
RightCM at -36.5 @ 10.568
RightLM at -54 @ -31.61
RightRM at -51 @ 0
RightCF at -54 @ 31.6102


