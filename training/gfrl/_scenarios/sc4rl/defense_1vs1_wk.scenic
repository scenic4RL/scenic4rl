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



MyGK at -98 @ 0
yellow_defender = MyRB

reg = get_reg_from_edges(-75, -85, 2, -2)

OpGK at 98 @ 0
ego = OpCF on LeftReg_CB, facing 90 deg

Ball ahead of ego by 2