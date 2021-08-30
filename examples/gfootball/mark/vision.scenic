from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False
param offsides = True
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# ----- Constants -----


# ----- Behaviors -----
behavior AIBehavior():
    do IdleBehavior() until (distance from ball to p1) < 0.8
    do BuiltinAIBot()

# ----- Regions -----

# for offside rule
right_back = get_reg_from_edges(80, 85, 40, 20)

# cluster
cluster_top_left = get_reg_from_edges(30, 75, 30, 10)

# player with ball
left_start = get_reg_from_edges(-10, 10, 20, 0)

# we have 2 players here
left_open_top_right = get_reg_from_edges(40, 60, -10, -35)


# ----- Players -----

# spawns = spawn_player_in_region(LeftReg_CM, 2, 1)
# for i in range(len(spawns)):
#     for j in range(i+1, len(spawns)):
#         print(i, j)
#         require (distance from spawns[i] to spawns[j]) >= min_dis
# print(spawns)
# print("a")
# require (distance from spawns[2] to spawns[0]) >= min_dis
# print("b")
# require (distance from spawns[2] to spawns[1]) >= min_dis
# print("c")

# Left
ego = LeftGK with behavior AIBehavior()

p1 = LeftPlayer with role "LM", in left_start, with behavior AIBehavior()
p2 = LeftPlayer with role "CF", in left_open_top_right, with behavior AIBehavior()
p3 = LeftPlayer with role "RM", in left_open_top_right, with behavior AIBehavior()

# Right
o0 = RightGK with behavior AIBehavior()
o1 = RightPlayer with role "RB", in right_back, with behavior AIBehavior()

# Mixed
left_roles = ("CB", "LB", "RB", "CB", "CB", "CM", "RM")
right_roles = ("CB", "CB", "LB", "CB", "CM", "CM", "CM", "LM", "CF")
mixed_left = []
mixed_right = []
for lr in left_roles:
    mixed_left.append(LeftPlayer with role lr, in cluster_top_left, with behavior AIBehavior())

for rr in right_roles:
    mixed_right.append(RightPlayer with role rr, in cluster_top_left, with behavior AIBehavior())

# Ball
ball = Ball ahead of p1 by 2
