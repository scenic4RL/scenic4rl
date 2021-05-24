from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

MyLeftMidRegion = get_reg_from_edges(-1, 5, 35, 30)
egoInitialRegion  = get_reg_from_edges(-40, -35, 5, -5)
egoAttackRegion = get_reg_from_edges(-80, -75, 5, 0)
blueRMAttackRegion = get_reg_from_edges(-80, -75, 5, -5)
fallBackRegion = get_reg_from_edges(-70, -60, 5, -5)

behavior egoBehavior(destination_point):
	passedToTeammate = False

	try:
		do dribbleToAndShoot(destination_point)

	interrupt when yellow_penaltyBox.containsPoint(self.position):
		print("case1")
		do AimGoalCornerAndShoot()

	interrupt when passedToTeammate and teammateHasBallPossession(self):
		print("case2")
		fallbackpoint = Point on fallBackRegion
		do MoveToPosition(fallbackpoint, sprint=True)
		do HoldPosition() until self.owns_ball

	interrupt when opponentTeamHasBallPossession(self):
		do FollowObject(ball, sprint=True)

	do IdleBehavior()


behavior blueRMBehavior(destination_point):

	try:
		do HighPassTo(ego)
		do MoveToPosition(destination_point, sprint=True)
		new_dest_point = Point on blueRMAttackRegion
		do egoBehavior(new_dest_point)
	interrupt when opponentTeamHasBallPossession(self):
		do FollowObject(ball, sprint=True)
	do IdleBehavior()

YellowGK with behavior HoldPosition()
yellow_defender1 = YellowRB
yellow_defender2 = YellowLM on MyLeftMidRegion

BlueGK
ego_destinationPoint = Point on egoAttackRegion
blueRM_destinationPoint = Point on blueRMAttackRegion

blueRM = BlueRM with behavior blueRMBehavior(blueRM_destinationPoint)
ego = BlueAM on egoInitialRegion, with behavior egoBehavior(ego_destinationPoint)

ball = Ball ahead of blueRM by 0.1
