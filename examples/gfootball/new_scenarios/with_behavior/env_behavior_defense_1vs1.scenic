from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle
import pdb

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1

behavior egoBehavior(destination_point):
	try:
		do dribbleToAndShoot(destination_point)
	interrupt when (distance from self to ball) > 2:
		do FollowObject(ball, sprint=True)
	do IdleBehavior()

defender_region = get_reg_from_edges(-52, -48, 5, -5)
attacker_region = get_reg_from_edges(-26, -22, 5, -5)

MyGK with behavior HoldPosition()
# yellow_defender = MyCB on defender_region

OpGK
ego = OpCM on attacker_region, with behavior egoBehavior(-80 @ 0)
ball = Ball ahead of ego by 0.1

yellow_defender = MyCB offset by -15 @ 5, with behavior HoldPosition()