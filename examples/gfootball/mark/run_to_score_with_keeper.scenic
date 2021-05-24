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

# -----Behavior-----
behavior dribble_evasive_zigzag(destination_point):
    # opponent = nearestOpponent(self)
    blueGK = opgk
    angleToblueGK = angle from self.position to blueGK.position
    current_heading = self.heading

    evade_direction = Uniform("left", "right")
    if evade_direction == "left":
        point_to_evadeTo = self offset along (Range(30,50) deg relative to current_heading) by 0 @ Range(50,60)
    else:
        point_to_evadeTo = self offset along (Range(-50,-30) deg relative to current_heading) by 0 @ Range(50,60)

    # print("point_to_evadeTo: ", point_to_evadeTo)
    while self.x <= blueGK.x and (blueGK.heading < 200 deg or blueGK.heading > 340):
        take MoveTowardsPoint(point_to_evadeTo, self.position)

    # print("end evasion behavior and exit")


behavior P1Behavior():
    # destination_point = Point in blue_penaltyBox
    ds = simulation().game_ds
    # print(player_with_ball(ds, ball))

    # destination_point = Point at 70 @ (Uniform(1) * Range(-28,-22))
    destination_point = Point at 99 @ 0
    evaded = False

    try:
        do MoveToPosition(destination_point, sprint=True)

    interrupt when blue_penaltyBox.containsPoint(ball.position):
        # print("Normal Shoot!")
        do AimGoalCornerAndShoot()

    interrupt when (not evaded) and (distance from self to opgk) < 40:
        evaded = True
        do dribble_evasive_zigzag(destination_point)

    do IdleBehavior()




# -----SET UP-----
ball = Ball at 2 @ 0

# Left Team
ego = YellowGK at -99 @ 0, with behavior IdleBehavior()
p1 = YellowCB at 0 @ 0, with behavior P1Behavior()

# Right Team
opgk = BlueGK at 99 @ 0
BlueLB at -12 @ 8.4
BlueCB at -12 @ 4.2
BlueCM at -12 @ 0
BlueCB at -12 @ -4.2
BlueRB at -12 @ -8.4
