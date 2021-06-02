from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
param game_duration = 400
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
# param end_episode_on_possession_change = True

LeftGK with behavior BuiltinAIBot()
leftLB = LeftLB with behavior BuiltinAIBot()
leftCB = LeftCB with behavior BuiltinAIBot()
leftRB = LeftRM with behavior BuiltinAIBot()
ego = RightGK at 90 @ -10, with behavior BuiltinAIBot()
RightCM at 20 @ 20, with behavior BuiltinAIBot()
RightAM at 25 @ 20,  with behavior BuiltinAIBot()
RightCF at -40 @ -10, with behavior BuiltinAIBot()
#RightCM with behavior BuiltinAIBot()
Ball ahead of ego by 2