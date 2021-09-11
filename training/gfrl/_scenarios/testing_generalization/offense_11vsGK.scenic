from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball at 0 @ 0 #center of the field

LeftGK
LeftLB 
LeftCB 
LeftCB 
LeftRB 
LeftLM
LeftCM 
LeftCM 
LeftRM 
LeftAM
LeftCF 

RightGK
