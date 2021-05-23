from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1

MyLeftMidRegion = get_reg_from_edges(-1, 5, 35, 30)
egoInitialRegion  = get_reg_from_edges(-40, -35, 5, -5)
egoAttackRegion = get_reg_from_edges(-80, -75, 5, 0)
opRMAttackRegion = get_reg_from_edges(-80, -75, 5, -5)
fallBackRegion = get_reg_from_edges(-70, -60, 5, -5)

behavior egoBehavior(destination_point):
	passedToTeammate = False

	try:
		do dribbleToAndShoot(destination_point)

	interrupt when yellow_penaltyBox.containsPoint(self.position):
		print("case1")
		if aimPointToShoot(self) is not None:
			do AimGoalCornerAndShoot()
			if self.owns_ball:
				do ShortPassTo(opRM)
		else:
			do ShortPassTo(nearestTeammate(self))
			passedToTeammate = True

	interrupt when passedToTeammate and teammateHasBallPossession(self):
		print("case2")
		fallbackpoint = Point on fallBackRegion
		do MoveToPosition(fallbackpoint, sprint=True)
		do HoldPosition() until self.owns_ball

	interrupt when opponentTeamHasBallPossession(self):
		do FollowObject(ball, sprint=True)

	do IdleBehavior()


behavior opRMBehavior(destination_point):

	try:
		do HighPassTo(ego)
		do MoveToPosition(destination_point, sprint=True)
		new_dest_point = Point on opRMAttackRegion
		do egoBehavior(new_dest_point)
	interrupt when opponentTeamHasBallPossession(self):
		do FollowObject(ball, sprint=True)
	do IdleBehavior()

MyGK with behavior HoldPosition()
yellow_defender1 = MyRB
yellow_defender2 = MyLM on MyLeftMidRegion

OpGK
ego_destinationPoint = Point on egoAttackRegion
opRM_destinationPoint = Point on opRMAttackRegion

opRM = OpRM with behavior opRMBehavior(opRM_destinationPoint)
ego = OpAM on egoInitialRegion, with behavior egoBehavior(ego_destinationPoint)

ball = Ball ahead of opRM by 0.1
