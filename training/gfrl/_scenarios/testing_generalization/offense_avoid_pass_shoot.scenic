from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


offset_direction = Range(-120, -60) deg

LeftGK 
ego = LeftAM on right_half_field
LeftCF at (ego offset along offset_direction by 0 @ Range(15,20))
Ball ahead of ego by 2

RightGK 
RightCB at (ego offset along offset_direction by 0 @ Range(5,10))