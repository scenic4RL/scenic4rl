from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
# from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
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

# Behaviors V2
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
                    # print("Shoot ", self)
                    take Shoot()
                else:
                    # print("Pass ", self)
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
    interrupt when (distance from self to opponent_goal_midpoint) <= MIN_SHOOT_DIS:
        take Shoot()


# Behaviors V1
behavior JustShoot():
    while True:
        if self.owns_ball:
            if (distance from self to opponent_goal_midpoint) < 30:
                shoot_option = Uniform("down", "up", "direct")
                if shoot_option == "down":
                    take SetDirection(6)
                elif shoot_option == "up":
                    take SetDirection(5)
                else:
                    pass

                take Shoot()
            else:
                take MoveTowardsPoint(opponent_goal_midpoint.x, opponent_goal_midpoint.y, self.x, self.y)

        else:
            take ReleaseDirection()

behavior JustPass():
    passed = False
    while True:
        if passed:
            take SetDirection(5)
            if not self.owns_ball:
                passed = False
        else:
            if self.owns_ball:
                # do PassToPlayer(p2, "short")
                take Pass()
                take SetDirection(5)
                passed = True
            else:
                take MoveTowardsPoint(ball.x, ball.y, self.x, self.y)


# Selection Behavior
behavior P1Behavior(selection, op, tp):
    if selection == "pass":
        do JustPass()
    else:
        do DynamicRunShoot(op, tp)

behavior P2Behavior(selection, op, tp):
    if selection == "pass":
        do JustShoot()
    else:
        do DynamicRunShoot(op, tp)


# target point in goal
tp = Point in opponent_goal

# ball at top
ball = Ball at 70 @ 28

OpGK at 99 @ 0
op = OpCB at 75 @ 30

ego = MyGK at -99 @ 0, with behavior IdleBehavior()
gk = ego

# select behavior
sel = Uniform("pass", "shoot")
# sel = "shoot"

# P2 Turing
p2 = MyCF at 70 @ 0, with behavior P2Behavior(sel, op, tp)
# P1 top with ball
p1 = MyCB at 70 @ 30, with behavior P1Behavior(sel, op, tp)

