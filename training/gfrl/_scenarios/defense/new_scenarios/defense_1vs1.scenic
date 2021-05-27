from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

YellowGK at 95 @ 40
yellow_defender = YellowRB

BlueGK at 95 @ 40
ego = BlueAM on LeftReg_CM

Ball ahead of ego by 0.5