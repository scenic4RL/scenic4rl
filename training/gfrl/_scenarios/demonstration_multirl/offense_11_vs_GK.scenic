from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# -----Constants-----
danger_cone_angle = 70 deg
danger_cone_radius = 20

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
    take MoveTowardsPoint(target_pt.position, self.position)

behavior PrimaryBehavior(destination_point, op):
    ds = simulation().game_ds
    while True:
        try:
            do MoveToPosition(destination_point, sprint=False)
        interrupt when right_penaltyBox.containsPoint(ds.ball.position):
            # print("Normal Shoot!, opgk pos: ", opponent_gk.position)
            do AimGoalCornerAndShoot()
        interrupt when (distance from self to op) < Range(8,20):
            take Pass()
            do RunToSafe(op, destination_point)

behavior SecondaryBehavior(destination_point, op):
    ds = simulation().game_ds
    while True:
        try:
            do MoveToPosition(destination_point, sprint=True)
        interrupt when (distance from self to ds.ball.position) < 2:
            do GreedyRS()



behavior GreedyRS():
    '''
    Always takes NoAction. Note it will not release direction.
    '''
    while True:
        if self.x < 75 or abs(self.y)>15:
            x = Range(80,90)
            y = Range(-5,5)

            if (distance from self to opgk) < 7:
                act =  Shoot()
                msg = " shoot"
            else:
                msg = f"move to {x:0.2f}, {y:0.2f}"
                dir = lookup_direction(x - self.x, y - self.y)
                action = SetDirection(dir)

        else:
            action = Shoot()
            #print("Close Enough, shoot")
            msg = "close enough"

        take action

# Selection Behavior
behavior P1Behavior(selection, op, tp):
    if selection == "shoot":
        do GreedyRS()
    else:
        do PrimaryBehavior(tp, op)

# target point in goal
tp = Point in right_goalRegion
sel = Uniform("pass", "shoot")
tp1 = Range(70,90) @ Range(15,25)
tp2 = Range(70,90) @ Range(-15,-25)

opgk = RightGK
ego = Ball at 0 @ 0
ball = ego

LeftGK at -98 @ 0 #, with behavior GreedyRS()
LeftLB at -60 @  30 #, with behavior GreedyRS()
LeftCB at -70 @  12 #, with behavior GreedyRS()
LeftCB at -70 @ -12 #, with behavior GreedyRS()
LeftRB at -60 @ -30 #, with behavior GreedyRS()
LeftLM at -25 @  15, with behavior SecondaryBehavior(tp1, opgk)
LeftCM at -50 @  10 #, with behavior GreedyRS()
LeftCM at -50 @ -10 #, with behavior GreedyRS()
LeftRM at -25 @ -15 #, with behavior GreedyRS()
LeftAM at -15 @ -2, with behavior SecondaryBehavior(tp2, opgk)
LeftCF at  -2 @ -1, with behavior P1Behavior("pass", opgk, tp)


