from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import BuiltinAIBot, IdleBehavior, JustShoot, JustPass

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True



ego = Ball at 75 @ 18

MyGK at -99 @ 0, with behavior BuiltinAIBot()
MyCB at 85 @ 0,  with behavior BuiltinAIBot()
MyCM at 75 @ 20, with behavior BuiltinAIBot()

OpGK at 99.5 @ -3
OpCB at 80 @ 20


#require always ego.x > 50