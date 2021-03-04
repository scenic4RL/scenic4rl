from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 25
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball in left_pbox

MyGK at -98 @ 0
MyCB in left_pbox


OpGK at 98 @ 0
OpCF in left_pbox
OpAM in left_pbox
