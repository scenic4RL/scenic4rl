from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball on RectangularRegion(20 @ 0, 0, 20, 20)

MyGK at -98 @ 0
MyCB on RectangularRegion(5 @ 0, 0, 10, 10)


OpGK at -98 @ -41

OpLB on RectangularRegion(-12 @ -20, 0, 10, 10)
OpCB on RectangularRegion(-12 @ -10, 0, 10, 10)
OpCM on RectangularRegion(-12 @ 0, 0, 10, 10)
OpCB on RectangularRegion(-12 @ 10, 0, 10, 10)
OpLB on RectangularRegion(-12 @ 20, 0, 10, 10)