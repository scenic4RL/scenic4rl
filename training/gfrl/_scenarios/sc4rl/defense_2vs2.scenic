from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


MyGK at 90 @ 40
yellow_defender1 = MyCB 
yellow_defender2 = MyCB 


OpGK at 95 @ 40
ego = OpCM on LeftReg_CM
bluePlayer = OpAM on LeftReg_CM

Ball ahead of ego by 0.5

#require (distance from yellow_defender1 to yellow_defender2) > 3
#require (distance from ego to bluePlayer) > 4