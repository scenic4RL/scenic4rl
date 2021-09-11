from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True

behavior dummy():
	do HoldPosition()



ego = Ball at 0 @ 0

LeftGK at -98 @  0, with behavior RunRight()
LeftAM at -5 @ -2, with behavior RunRight()
LeftCF at -10 @  10, with behavior RunRight()
LeftRM at - 10 @ 20, with behavior RunRight()
LeftCF at -10 @  -10, with behavior RunRight()
LeftRM at - 10 @ -20, with behavior RunRight()

RightGK at 98 @ 0, with behavior RunRight()
RightCB at 50 @ -20, with behavior RunRight()
RightCB at 50 @  20, with behavior RunRight()
