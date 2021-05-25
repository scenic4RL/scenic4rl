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
ego = YellowGK at -99 @ 0, with behavior IdleBehavior()
YellowLB at -67.2 @ 19.576
YellowCB at -75 @ 6.356
YellowCB at -75 @ -6.3559
YellowRB at -67.2 @ -19.576
YellowCM at -43.4 @ 10.568
YellowCM at -43.4 @ -10.568
YellowCM at 50 @ 31.61
YellowLM at 25 @ 10
YellowRM at 25 @ -10
YellowCF at 35 @ -31.61


# Right Team
opgk = BlueGK at 99 @ 0
BlueLB at -12.8 @ -19.576
BlueCB at -40 @ -6.356
BlueCB at 40 @ 6.3559
BlueRB at -12.8 @ -19.576
BlueCM at -36.5 @ -10.568
BlueCM at -28.2 @ 0
BlueCM at -36.5 @ 10.568
BlueLM at -54 @ -31.61
BlueRM at -51 @ 0
BlueCF at -54 @ 31.6102


