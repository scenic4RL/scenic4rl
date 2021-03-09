from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = False
param right_team_difficulty = 1.0
#param render = False

ball = Ball at 10 @ 12

ego = MyGK at -98 @ 0
MyCF at 70 @ 0
MyAM at 70 @ 30

OpGK at 98 @ 0
op1 = OpCB at 75 @ 10
op2 = OpAM at 65 @ 10
op3 = OpCM at 55 @ 10
op4 = OpCF at 45 @ 10

right_half =  RectangularRegion(50 @ 0, 0, 100, 84)

#require always ball in right_half
#require op1 in right_half
#require op2 in right_half
#require op3 in right_half
#require op4 in right_half

#require op1.position.x > 0
#require op2.position.x > 0
#require op3.position.x > 0
#require op4.position.x > 0