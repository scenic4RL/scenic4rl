from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = False

# ----- Constants -----
init_target_distance = 35

danger_cone_angle = 80 deg
danger_cone_radius = 20

pass_distance = 10

behavior PassRunReceive(target_point):
    ds = simulation().game_ds
    teammate, _ = get_closest_player_dis(self.position, ds.my_players)

    do FollowObject(ball) until self.owns_ball
    do PassToPlayer(teammate, "short")
    print("first pass. Now start running")
    do MoveToPosition(target_point.x, target_point.y, sprint=True) until self.owns_ball
    print("received ball")

    do IdleBehavior() for 2 seconds
    terminate


behavior SafePass():
    while True:
        if not self.owns_ball:
            print("No Ball!!!")
        else:
            danger_cone = SectorRegion(self, danger_cone_radius, self.heading, danger_cone_angle)
            safe_players = [p for p in simulation().game_ds.my_players if p not in danger_cone]
            print("pass")
            do PassToPlayer(get_closest_player_dis(self.position, safe_players)[0], "short")
            break

behavior WaitThenPass():
    ds = simulation().game_ds
    try:
        do IdleBehavior()
    interrupt when (self.owns_ball and get_closest_player_dis(self.position, ds.op_players)[1] < pass_distance):
        do SafePass()

# ----- Set up players -----
ego = MyGK facing toward right_goal_midpoint, with behavior IdleBehavior()
o0 = OpGK facing toward left_goal_midpoint, with behavior IdleBehavior()

p1_pos = Point on workspace
relative_target_heading = Range(-179,179) deg
target_pos = Point at p1_pos offset along relative_target_heading by 0 @ init_target_distance
require (target_pos in workspace)

o1_pos = Point at p1_pos offset along relative_target_heading by 0 @ init_target_distance/2
require (o1_pos in workspace)

# spawn teammates on the sides
teammate_h = Uniform(-1,1) * danger_cone_angle/2 relative to relative_target_heading
teammate_pt = Point at p1_pos offset along teammate_h by 0 @ danger_cone_radius
require (teammate_pt in workspace)

ball = Ball ahead of p1_pos by 3
p1 = MyPlayer with role "CM", at p1_pos, with behavior PassRunReceive(target_pos)
p2 = MyPlayer with role "CM", at teammate_pt, with behavior WaitThenPass()
o1 = OpPlayer with role "CM", at o1_pos, with behavior FollowObject(ball, opponent=True)


