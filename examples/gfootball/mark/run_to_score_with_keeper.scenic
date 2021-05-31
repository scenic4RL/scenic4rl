from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True
# -----Constants-----
max_shoot_distance = 30 # if empty goal
shoot_distance = 25 # normal
# -----Behavior-----
behavior dribble_evasive_zigzag(destination_point, opponent_gk):
    # opponent = nearestOpponent(self)
    blueGK = opponent_gk
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
    opponent_gk = None
    for p in ds.right_players:
        if p.role=="GK":
            opponent_gk = p

    # destination_point = Point at 70 @ (Uniform(1) * Range(-28,-22))
    destination_point = Point at 99 @ 0
    evaded = False
    # print("Initial gk:", opponent_gk.position)
    try:
        do MoveToPosition(destination_point, sprint=True)
    interrupt when (not evaded) and (distance from self.position to opponent_gk) < 40:
        evaded = True
        # print("Evade, evaded:", evaded, opponent_gk.position)
        do dribble_evasive_zigzag(destination_point, opponent_gk)
    interrupt when right_penaltyBox.containsPoint(ds.ball.position):
        # print("Normal Shoot!, opgk pos: ", opponent_gk.position)
        do AimGoalCornerAndShoot()
    do IdleBehavior()

# -----SET UP-----
Ball at 2 @ 0
# Left Team
ego = LeftGK at -99 @ 0, with behavior IdleBehavior()
p1 = LeftCB at 0 @ 0, with behavior P1Behavior()
# Right Team
RightGK at 99 @ 0
RightLB at -12 @ 20
RightCB at -12 @ 10
RightCM at -12 @ 0
RightCB at -12 @ -10
RightRB at -12 @ -20
