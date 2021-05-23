from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# -----Constants-----
max_shoot_distance = 30 # if empty goal
shoot_distance = 25 # normal


def can_shoot(me, ops, target_point, shoot_distance):
    if not me.owns_ball:
        return False
    if (distance from me to target_point) > shoot_distance:
        return False
    goal_relative_heading = angle from me to target_point
    shoot_cone = SectorRegion(me, shoot_distance, goal_relative_heading, 40 deg)  # center, radius, heading, angle
    # if (distance from me to target_point) < MIN_SHOOT_DIS:
    #     return True
    return all([op not in shoot_cone for op in ops])

# -----Behavior-----
behavior AimGoalCornerAndShoot():
    aimPoint = aimPointToShoot(self)
    is_player_opponent = self.team == "opponent"
    take MoveTowardsPoint(aimPoint, self.position, is_player_opponent)
    take Shoot()
    take ReleaseSprint()
    take ReleaseDirection()

behavior AimGoalCenterAndShoot():
    take MoveTowardsPoint(opponent_goal_midpoint, self.position)
    take Shoot()
    take ReleaseSprint()
    take ReleaseDirection()

behavior dribble_evasive_zigzag(destination_point):
    # opponent = nearestOpponent(self)
    opponent = opgk
    angleToOpponent = angle from self.position to opponent.position
    current_heading = self.heading
    print("current position: ", self.position)

    if angleToOpponent > 0: # if the opponent is on the right side of self player executing this behavior
        print("turn to left")
        point_to_evadeTo = self offset along (-45 deg relative to current_heading) by 0 @ 60
    else:
        print("turn to right")
        point_to_evadeTo = self offset along (45 deg relative to current_heading) by 0 @ 60

    print("point_to_evadeTo: ", point_to_evadeTo)
    while self.x <= opponent.x:
        take MoveTowardsPoint(point_to_evadeTo, self.position)

    print("end evasion behavior and exit")
    # print("destination_point: ", destination_point)
    # do MoveToPosition(destination_point, sprint =True) # zag behavior


behavior CloseIn(destination_point):
    evaded = False
    try:
        do MoveToPosition(destination_point, sprint=True)
        print("Close In!")
        do MoveToPosition(opponent_goal_midpoint, sprint=True)

    interrupt when (not evaded) and (distance from self to opgk) < 40:
        # take ReleaseSprint()
        evaded = True
        do dribble_evasive_zigzag(destination_point)


behavior P1Behavior():
    # destination_point = Point in opponentTeam_penaltyBox
    ds = simulation().game_ds
    # destination_point = Point at 70 @ (Uniform(1) * Range(-28,-22))
    destination_point = Point at 99 @ 0

    try:
        do CloseIn(destination_point)

    interrupt when can_shoot(self, ds.op_players, opponent_goal_midpoint, max_shoot_distance):
        print("Clear to shoot")
        do AimGoalCenterAndShoot()

    interrupt when (distance from ball to opponent_goal_midpoint) < shoot_distance:
        print("Normal Shoot!")
        do AimGoalCornerAndShoot()

    do IdleBehavior()




# -----SET UP-----
ball = Ball at 2 @ 0

# Left Team
ego = MyGK at -99 @ 0, with behavior IdleBehavior()
p1 = MyCB at 0 @ 0, with behavior P1Behavior()

# Right Team
opgk = OpGK at 99 @ 0
OpLB at -12 @ 8.4
OpCB at -12 @ 4.2
OpCM at -12 @ 0
OpCB at -12 @ -4.2
OpRB at -12 @ -8.4
