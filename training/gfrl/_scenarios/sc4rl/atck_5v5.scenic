from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ball = Ball

MyGK at -98 @ 0
ego = MyCF at -2 @ 0
MyLM at -25 @  15
MyRM at -25 @ -15


OpGK at  98 @ 0
OpCF at   10 @ 0
OpLM at  25 @ -15
OpRM at  25 @  15