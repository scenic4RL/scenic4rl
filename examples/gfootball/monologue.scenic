from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 100
param deterministic = False
param offsides = False
param end_episode_on_score = False
param end_episode_on_out_of_play = False
param end_episode_on_possession_change = False


behavior JustPass():
	while True:
		take Pass()

behavior RunRight():
	while True:
		take SetDirection(5)

behavior JustShoot():
	while True:
		take Shoot()

behavior BuiltinAIBot():
	while True:
		take BuiltinAIAction()



ego = Ball at 0 @ 0

MyGK at -98 @ 0  ,  with behavior BuiltinAIBot()
MyCF at   -2 @ 0 ,  with behavior BuiltinAIBot()
MyAM at -25 @  5 ,  with behavior BuiltinAIBot()

OpGK at  98 @ 0     ,  with behavior BuiltinAIBot()
OpCF at   10 @ 0 ,  with behavior BuiltinAIBot()
OpAM at  25 @  -5 ,  with behavior BuiltinAIBot()
