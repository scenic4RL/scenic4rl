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

behavior dribble_evasive_zigzag(destination_point):
    # opponent = nearestOpponent(self)
    opponent = opgk
    angleToOpponent = angle from self.position to opponent.position
    current_heading = self.heading

    evade_direction = Uniform("left", "right")
    if evade_direction == "left":
        point_to_evadeTo = self offset along (Range(30,50) deg relative to current_heading) by 0 @ Range(50,60)
    else:
        point_to_evadeTo = self offset along (Range(-50,-30) deg relative to current_heading) by 0 @ Range(50,60)

    # print("point_to_evadeTo: ", point_to_evadeTo)
    while self.x <= opponent.x and (opponent.heading < 200 deg or opponent.heading > 340):
        take MoveTowardsPoint(point_to_evadeTo, self.position)

    # print("end evasion behavior and exit")


behavior P1Behavior():
    # destination_point = Point in opponentTeam_penaltyBox
    ds = simulation().game_ds
    # destination_point = Point at 70 @ (Uniform(1) * Range(-28,-22))
    destination_point = Point at 99 @ 0
    evaded = False

    try:
        do MoveToPosition(destination_point, sprint=True)

    interrupt when opponentTeam_penaltyBox.containsPoint(ball.position):
        # print("Normal Shoot!")
        do AimGoalCornerAndShoot()

    interrupt when (not evaded) and (distance from self to opgk) < 40:
        evaded = True
        do dribble_evasive_zigzag(destination_point)

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
