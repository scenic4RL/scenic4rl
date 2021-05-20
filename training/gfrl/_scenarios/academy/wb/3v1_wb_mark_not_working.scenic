from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

danger_cone_angle = 70 deg
danger_cone_radius = 10

pass_distance = 10
SHOOT_DIS = 30

def is_danger(me, op):
    rheading = angle from me to op
    danger_cone = SectorRegion(me, danger_cone_radius, rheading, danger_cone_angle) # center, radius, heading, angle
    return (op in danger_cone)


behavior RunToSafe(op):
    # run to safe location based on op location
    relative_heading = angle from self to op
    h_a = -danger_cone_angle/2 relative to relative_heading
    h_b = danger_cone_angle/2 relative to relative_heading
    pt_a = Point at self offset along h_a by 0 @ danger_cone_radius
    pt_b = Point at self offset along h_b by 0 @ danger_cone_radius
    target_pt = pt_a
    if (distance from pt_a to right_goal_midpoint) > (distance from pt_b to right_goal_midpoint):
        target_pt = pt_b
    take MoveTowardsPoint(target_pt.x, target_pt.y, self.x, self.y)

behavior PassIfNoShoot(op):
    can_pass = True
    while True:
        if not self.is_controlled:
            take NoAction()
            continue

        if self.owns_ball:
            # check if clear to shoot
            if (distance from self to right_goal_midpoint) <= (SHOOT_DIS + 2):
                goal_relative_heading = angle from self to right_goal_midpoint
                danger_cone = SectorRegion(self, SHOOT_DIS, goal_relative_heading, 40 deg)  # center, radius, heading, angle
                if op not in danger_cone:
                    # print("Shoot ", self)
                    take Shoot()
                else:
                    # pass to player
                    if can_pass:
                        do SafePass()
                        can_pass = False
                    else:
                        # print("idle close, ", self)
                        take NoAction()
            else:
                # far. Should close in
                # print("Close in")
                try:
                    do RunToSafe(op) until ((distance from self to right_goal_midpoint) <= SHOOT_DIS)
                    can_pass = True
                interrupt when (self.owns_ball and is_danger(self, op)):
                    # pass to player
                    if can_pass:
                        do SafePass()
                        can_pass = False
                    else:
                        # print("idle, ", self)
                        take NoAction()

        else: # if not own ball
            do FollowObject(ball) until self.owns_ball
            # take NoAction()
            # do RunToSafe(op)

behavior SafePass():
    danger_cone = SectorRegion(self, danger_cone_radius, self.heading, danger_cone_angle)
    safe_players = [p for p in simulation().game_ds.my_players if p not in danger_cone]
    # print("pass")

    if not self.owns_ball:
        # print("Should not happen. No ball in pass.")
        take MoveTowardsPoint(right_goal_midpoint.x, right_goal_midpoint.y, self.x, self.y)
    else:
        target_p = get_closest_player_dis(self.position, safe_players)[0]
        do PassToPlayer(target_p, "short")
        # print("Pass ", self)
        # take Pass()

behavior FirstPassThenNormal(op):
    # take Pass()
    # take Pass()
    do PassIfNoShoot(op)



ball = Ball at 62 @ 0

ego = MyGK at -99 @ 0, with behavior IdleBehavior()
o0 = OpGK at 99 @ 0
o1 = OpCB at 75 @ 0

# mid
p1 = MyCM at 60 @ 0, with behavior FirstPassThenNormal(o1)
# top
p2 = MyCM at 70 @ 20, with behavior PassIfNoShoot(o1)
# bot
p3 = MyCM at 70 @ -20, with behavior PassIfNoShoot(o1)