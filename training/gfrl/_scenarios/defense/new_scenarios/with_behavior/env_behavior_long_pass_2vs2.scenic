from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param right_team_difficulty = 1
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

MyLeftMidRegion = get_reg_from_edges(-1, 5, 35, 30)
egoInitialRegion  = get_reg_from_edges(-40, -35, 5, -5)
egoAttackRegion = get_reg_from_edges(-80, -75, 5, 0)
rightRMAttackRegion = get_reg_from_edges(-80, -75, 5, -5)
fallBackRegion = get_reg_from_edges(-70, -60, 5, -5)

behavior egoBehavior(destination_point):
	passedToTeammate = False

	try:
		do dribbleToAndShoot(destination_point)

	interrupt when left_penaltyBox.containsPoint(self.position):
		do AimGoalCornerAndShoot()

	interrupt when passedToTeammate and teammateHasBallPossession(self):
		fallbackpoint = Point on fallBackRegion
		do MoveToPosition(fallbackpoint, sprint=True)
		do HoldPosition() until self.owns_ball

	interrupt when opponentTeamHasBallPossession(self):
		do FollowObject(ball, sprint=True)

	do HoldPosition()


behavior rightRMBehavior(destination_point):

	try:
		do HighPassTo(ego)
		do MoveToPosition(destination_point, sprint=True)
		new_dest_point = Point on rightRMAttackRegion
		do egoBehavior(new_dest_point)
	interrupt when opponentTeamHasBallPossession(self):
		do FollowObject(ball, sprint=True)
	do HoldPosition()

LeftGK with behavior HoldPosition()
left_defender1 = LeftRB
left_defender2 = LeftLM on MyLeftMidRegion

RightGK
ego_destinationPoint = Point on egoAttackRegion
rightRM_destinationPoint = Point on rightRMAttackRegion

rightRM = RightRM with behavior rightRMBehavior(rightRM_destinationPoint)
ego = RightAM on egoInitialRegion, with behavior egoBehavior(ego_destinationPoint)

ball = Ball ahead of rightRM by 2
