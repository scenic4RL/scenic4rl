from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


ego = Ball on RectangularRegion(70 @ 28, 0, 5, 5)

MyGK at -99 @ 0
MyCB on RectangularRegion(70 @ 0, 0, 5, 5)
MyCB on RectangularRegion(70 @ 30, 0, 5, 5)


OpGK on RectangularRegion(98 @ 0, 0, 2, 4)
OpCB on RectangularRegion(75 @ 30, 0, 5, 5)