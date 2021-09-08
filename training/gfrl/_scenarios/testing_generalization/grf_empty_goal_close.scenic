from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

RightGK at -99 @ -41
LeftGK at -99 @ 0

# we initially place the player anywhere on the right penalty box region to score
ego = LeftCB on right_penaltyBox
Ball ahead of ego by 2