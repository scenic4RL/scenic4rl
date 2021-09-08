from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 3000
param deterministic = False
param offsides = False
param right_team_difficulty = 0.05

ego = Ball at 0 @ 0


LeftGK at      -99 @ 0
LeftRM at  		 0 @ -2
LeftCF at  0 @  2
LeftLB at -42.2000 @  19.5760
LeftCB at -50 @  6.3560
LeftCB at -50 @ -6.3559
LeftRB at -42.2000 @ -19.5760
LeftCM at -18.4212 @  10.5680
LeftCM at -26.7574 @ 0
LeftCM at -18.4212 @ -10.5680
LeftLM at -1 @  21.6100

RightGK at 99.0000 @  0
RightRM at  5.0000 @  0
RightCF at  1.0000 @  21.6102
RightLB at 42.2000 @ -19.5760
RightCB at 50.0000 @ -6.3560
RightCB at 50.0000 @  6.3559
RightRB at 42.2000 @  19.5760
RightCM at 18.4212 @ -10.5680
RightCM at 26.7574 @  0
RightCM at 18.4212 @  10.5680
RightLM at  1.0000 @ -21.6100
