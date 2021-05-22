from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle
import pdb

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1


behavior dribble_evasive_zigzag(destination_point):
	opponent = nearestOpponent(self)
	angleToOpponent = angle from self.position to opponent.position
	current_heading = self.heading
	print("current position: ", self.position)

	if angleToOpponent > 0: # if the opponent is on the right side of self player executing this behavior
		print("turn to left")
		point_to_evadeTo = self offset along (-45 deg relative to current_heading) by 0 @ Range(5,15)
	else: 
		print("turn to right")
		point_to_evadeTo = self offset along (45 deg relative to current_heading) by 0 @ Range(5,15)

	print("point_to_evadeTo: ", point_to_evadeTo)
	do MoveToPosition(point_to_evadeTo) # zig behavior
	print("end evasion behavior and start returning to destination_point")
	print("destination_point: ", destination_point)
	do MoveToPosition(destination_point, sprint =True) # zag behavior

# behavior evadeOpponentAndShoot(destination_point):
# 	opponent = nearestOpponent(self)
# 	is_player_opponent = self.team is "opponent"

# 	print("start dribble_evasive_zigzag")
# 	do dribble_evasive_zigzag(destination_point) until abs(self.position.y - opponent.position.y) > 1
# 	print("end dribble_evasive_zigzag")

# 	if abs(self.position.y - opponent.position.y) > 1:
# 		print("case1")
# 		take MoveTowardsPoint(penaltyBox_myteam_center, opponent=is_player_opponent)
# 		take Shoot()
# 	else:
# 		print("case2")
# 		point_to_evadeTo = self.position.x @ destination_point.y
# 		do MoveToPosition(point_to_evadeTo, sprint=True) until abs(self.position.y - opponent.position.y) > 1

# 		aimPoint = aimPointToShoot(self)
# 		take MoveTowardsPoint(aimPoint, opponent=is_player_opponent)
# 		take Shoot()

# 	take ReleaseDirection()
# 	take ReleaseSprint()
# 	print("end evadeOpponentAndShoot")


	# do IdleBehavior()
	
	# if angleToOpponent > 0:
	# 	turn_direction = -1
	# else:
	# 	turn_direction = 1

	# corresponding_dir = (corresponding_dir + 1 * turn_direction) % 9
	# take SetDirection(corresponding_dir)
	# do IdleBehavior() until abs(self.position.y - yellow_defender.position.y) > 1 or abs(self.position.y) > 10
	# # do IdleBehavior() until (distance from self to yellow_defender) < 1 or abs(self.position.y) > 10

	# if abs(self.position.y - yellow_defender.position.y) > 1:
	# 	corresponding_dir = (corresponding_dir - 1 * turn_direction) % 9
	# 	take SetDirection(corresponding_dir)
	# 	take Shoot()
	# else:
	# 	if turn_direction == 1:
	# 		direction = 7
	# 	else:
	# 		direction = -7

	# 	corresponding_dir = (corresponding_dir + direction) % 9
	# 	take SetDirection(corresponding_dir)
	# 	take Sprint()
	# 	do IdleBehavior() until abs(self.position.y - yellow_defender.position.y) > 0.5 and abs(self.position.y) < abs(yellow_defender.position.y) \
	# 							or abs(self.position.y) <= 10 
	# 	take ReleaseSprint()
		
	# 	sign = 1 if turn_direction > 0 else -1
	# 	corresponding_dir = (corresponding_dir + 2 * sign) % 9
	# 	take SetDirection(corresponding_dir)
	# 	take Shoot()

behavior AimGoalCornerAndShoot():
	aimPoint = aimPointToShoot(self)
	is_player_opponent = self.team is "opponent"
	take MoveTowardsPoint(aimPoint, self.position, is_player_opponent)
	take Shoot()
	take ReleaseSprint()
	take ReleaseDirection()

behavior dribbleTo(destination_point):
	# had_ball_possession = False
	try:
		do MoveToPosition(destination_point)
	interrupt when opponentInRunway(self, radius=Range(5,10)):
		# had_ball_possession = True
		do dribble_evasive_zigzag(destination_point)
	interrupt when myTeam_penaltyBox.containsPoint(ball.position):
		do AimGoalCornerAndShoot()
	interrupt when (distance from self to ball) > 2:
		do FollowObject(ball, sprint=True)
	do IdleBehavior()


defender_region = get_reg_from_edges(-52, -48, 5, -5)
attacker_region = get_reg_from_edges(-26, -22, 5, -5)

MyGK at 95 @ 40, with behavior IdleBehavior()
# yellow_defender = MyCB on defender_region

OpGK at 95 @ 40, with behavior IdleBehavior()
ego = OpCM on attacker_region, with behavior dribbleTo(-80 @ 0)
ball = Ball ahead of ego by 0.1

# yellow_defender = MyCB offset by -15 @ 6, with behavior IdleBehavior()