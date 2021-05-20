from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.core.geometry import normalizeAngle
import pdb

param game_duration = 600
param deterministic = False
param offsides = False
param right_team_difficulty = 1


behavior dribble_evasive_turn():
	corresponding_dir = currentDirectionIndex(self)
	angleToOpponent = angle from self.position to yellow_defender.position
	is_player_opponent = self.team is "opponent"
	current_heading = self.heading

	if angleToOpponent > 0: # if the opponent is on the right side of self player executing this behavior
		print("turn to left")
		destination_point = self offset along (-45 deg relative to current_heading) by 0 @ Range(10,15)
	else: 
		print("turn to right")
		destination_point = self offset along (45 deg relative to current_heading) deg by 0 @ Range(10,15)

	print("angleToOpponent: ", angleToOpponent)
	print("self.position: ", self.position)
	print("self.heading: ", self.heading * 180 / 3.1412)
	print("destination_point: ", destination_point)

	do MoveToPosition(destination_point, opponent=is_player_opponent)
	do IdleBehavior()
	
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

	take ReleaseDirection()
	take ReleaseSprint()


behavior dribbleTo(destination_point):
	player_type = self.team is 'opponent'
	
	try:
		do MoveToPosition(destination_point, opponent=player_type)
	interrupt when opponentInRunway(self, radius=Range(10,12)):
		do dribble_evasive_turn()
	interrupt when left_pbox.containsPoint(ball.position):
		take Shoot()
		take ReleaseSprint()
		take ReleaseDirection()
		do IdleBehavior()


defender_region = get_reg_from_edges(-52, -48, 5, -5)
attacker_region = get_reg_from_edges(-26, -22, 5, -5)

MyGK at 95 @ 40, with behavior IdleBehavior()
yellow_defender = MyCB on defender_region

OpGK at 95 @ 40, with behavior IdleBehavior()
ego = OpCM on attacker_region, with behavior dribbleTo(-80 @ 0)
ball = Ball ahead of ego by 0.5

# yellow_defender = MyCB offset by -15 @ 6, with behavior IdleBehavior()