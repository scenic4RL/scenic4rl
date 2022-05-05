from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# Constants
danger_cone_angle = 60 deg
danger_cone_radius = 20

SHOOT_DIS = 25
MIN_SHOOT_DIS = 8

def can_shoot(me):
    goal_relative_heading = angle from me to right_goal_midpoint
    shoot_cone = SectorRegion(me, SHOOT_DIS, goal_relative_heading, 40 deg)  # center, radius, heading, angle
    if (distance from me to right_goal_midpoint) < MIN_SHOOT_DIS:
        return True
    return (opcb not in shoot_cone and (distance from me to right_goal_midpoint) < SHOOT_DIS)


behavior RunToSafe():
    target_point = right_goal_midpoint
    # run to safe location based on op location
    relative_heading = angle from self to opcb
    h_a = -danger_cone_angle/2 relative to relative_heading
    h_b = danger_cone_angle/2 relative to relative_heading
    pt_a = Point at self offset along h_a by 0 @ danger_cone_radius
    pt_b = Point at self offset along h_b by 0 @ danger_cone_radius
    target_pt = pt_a
    if (distance from pt_a to target_point) > (distance from pt_b to target_point):
        target_pt = pt_b
    if self.position.x < opcb.position.x:
        take MoveTowardsPoint(target_pt.position, self.position)
    else:
        take ReleaseDirection()


behavior PassAndWait(tp1, tp2, teammate):
    ds = simulation().game_ds
    # print(f"Move {self.position}")
    # do MoveToPosition(tp, sprint=True)
    #
    # if opponentInRunway(self, 5):
    #     print(f"Pass {self.position}")
    # do ShortPassTo(teammate)

    while True:
        try:
            do MoveToPosition(tp1, sprint=True)
            do MoveToPosition(tp2, sprint=False)

        interrupt when self.owns_ball and can_shoot(teammate):
            # print("Pass!")
            do ShortPassTo(teammate)

        interrupt when self.owns_ball and can_shoot(self):
            # print("Shoot!")
            # take Shoot()
            do AimGoalCornerAndShoot()


behavior ReceiverBehavior(tp):
    ds = simulation().game_ds
    while True:
        try:
            do MoveToPosition(tp, sprint=False)
            do RunToSafe()

        interrupt when self.owns_ball:
            # print("Shoot!")
            do AimGoalCornerAndShoot()

        # interrupt when self.owns_ball and (distance from self to opcb) < Range(4, 10):
        #     print("Pass!")
        #     do ShortPassTo(teammate)



# target point in goal
tp1 = Range(60,65) @ Range(5,15)
tp2 = Point in right_goalRegion
tp_teammate = Range(80,88) @ Range(0,-10)

ball = Ball at 52 @ 0
ego = ball

opgk = RightGK at  98 @   0
opcb = RightCB at  70 @  -5

mygk = LeftGK at -98 @  0
mycf = LeftCF at 80 @ -10, with behavior ReceiverBehavior(tp_teammate)
# with ball
myam = LeftAM at 50 @  0, with behavior PassAndWait(tp1, tp2, mycf)




