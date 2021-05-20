from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
# from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True
# Constants
danger_cone_angle = 70 deg
danger_cone_radius = 20
pass_distance = 10
SHOOT_DIS = 20
MIN_SHOOT_DIS = 8
def is_danger(me, op):
    rheading = angle from me to op
    danger_cone = SectorRegion(me, danger_cone_radius, rheading, danger_cone_angle) # center, radius, heading, angle
    return (op in danger_cone)
def can_shoot(me, op, target_point):
    goal_relative_heading = angle from me to target_point
    shoot_cone = SectorRegion(me, SHOOT_DIS, goal_relative_heading, 40 deg)  # center, radius, heading, angle
    if (distance from me to target_point) < MIN_SHOOT_DIS:
        return True
    return (op not in shoot_cone and (distance from me to target_point) < SHOOT_DIS)
# Behaviors
behavior CloseInAndAct(op, target_point):
    can_pass = True
    while True:
        if self.owns_ball:
            # check if good to shoot
            if can_shoot(self, op, target_point):
                take ReleaseDribble()
                # act = Uniform("shoot", "pass")
                act = "shoot"
                if act == "shoot":
                    #print("Shoot ", self)
                    take Shoot()
                else:
                    #print("Pass ", self)
                    if can_pass:
                        take Pass()
                        can_pass = False
                    else:
                        take ReleaseDirection()
            else:
                take Dribble()
                do RunToSafe(op, target_point)
                # take MoveTowardsPoint(target_point.x, target_point.y, self.x, self.y)
                #take ReleaseDirection()
        else:
            take ReleaseDirection()
# behavior SafePass():
#     danger_cone = SectorRegion(self, danger_cone_radius, self.heading, danger_cone_angle)
#     safe_players = [p for p in simulation().game_ds.my_players if p not in danger_cone]
#
#     if not self.owns_ball:
#         take MoveTowardsPoint(right_goal_midpoint.x, right_goal_midpoint.y, self.x, self.y)
#     else:
#         target_p = get_closest_player_dis(self.position, safe_players)[0]
#         do PassToPlayer(target_p, "short")
#
behavior RunToSafe(op, target_point):
    # run to safe location based on op location
    relative_heading = angle from self to op
    h_a = -danger_cone_angle/2 relative to relative_heading
    h_b = danger_cone_angle/2 relative to relative_heading
    pt_a = Point at self offset along h_a by 0 @ danger_cone_radius
    pt_b = Point at self offset along h_b by 0 @ danger_cone_radius
    target_pt = pt_a
    if (distance from pt_a to target_point) > (distance from pt_b to target_point):
        target_pt = pt_b
    take MoveTowardsPoint(target_pt.x, target_pt.y, self.x, self.y)
behavior DynamicRunShoot(op, target_point):
    try:
        do CloseInAndAct(op, target_point)
    interrupt when (distance from self to right_goal_midpoint) <= MIN_SHOOT_DIS:
        take Shoot()
# behavior DynamicRunShoot(op, target_point):
#     while True:
#         if self.owns_ball:
#             if (distance from self to right_goal_midpoint) <= MIN_SHOOT_DIS:
#                 take Shoot()
#             do CloseInAndAct(op, target_point)
#
#         else:
#             take ReleaseDirection()
# target point in goal
tp = Point in right_goal
# ball at top
ball = Ball at 70 @ 28

OpGK at 99 @ 0
op = OpCB at 75 @ 30

ego = MyGK at -99 @ 0, with behavior IdleBehavior()
gk = ego
# P2 Turing
p2 = MyCB at 70 @ 0, with behavior DynamicRunShoot(op, tp)
# P1 top with ball
p1 = MyCB at 70 @ 30, with behavior DynamicRunShoot(op, tp)

