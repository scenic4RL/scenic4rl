from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1

MyLeftMidRegion = get_reg_from_edges(-1, 5, 35, 30)
OpAttackRegion  = get_reg_from_edges(-40, -35, 5, -5)

MyGK at 95 @ -40, with behavior IdleBehavior()
yellow_defender1 = MyRB
yellow_defender2 = MyLM on MyLeftMidRegion

OpGK at 90 @ -40, with behavior IdleBehavior()
ego = OpRM
attacking_opponent = OpAM on OpAttackRegion

Ball ahead of ego by 0.5
