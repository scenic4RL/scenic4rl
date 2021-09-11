from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = True
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# ----- Constants -----


# ----- Behaviors -----
def offside_x(op_players):
    # offside line is determined by the second last opponent player.
    # https://en.wikipedia.org/wiki/Offside_(association_football)
    all_x = sorted([p.position.x for p in op_players if p.position.x < 100], reverse=True)
    return all_x[1]

behavior avoidOffside():
    ds = simulation().game_ds
    while True:
        if not self.owns_ball:
            max_x = offside_x(ds.right_players)
            if self.position.x >= (max_x - 2):
                take SetDirection(1) # our left
            elif self.position.x < (max_x - 5):
                take SetDirection(5) # our right
            else:
                take ReleaseDirection()
        else:
            # RL takes control
            do IdleBehavior()





# ----- Regions -----

# for offside rule
right_back = get_reg_from_edges(80, 85, -40, -30)

# cluster
# (0+-100, 0+-42)
cluster_top_right = get_reg_from_edges(20, 65, -40, -30)

# player with ball
left_start = get_reg_from_edges(10, 15, -5, 5)

# open: we have 2 players here
left_open_top_left = get_reg_from_edges(70, 80, -10, 0)


# ----- Players -----

# Left
ego = LeftGK

p1 = LeftPlayer with role "RM", in left_start
p2 = LeftPlayer with role "CF", with behavior avoidOffside(), in left_open_top_left, with width 1.5, with length 1.5
p3 = LeftPlayer with role "LM", with behavior avoidOffside(), in left_open_top_left, with width 1.5, with length 1.5

# Right
o0 = RightGK
o1 = RightPlayer with role "LB", in right_back

# Mixed
left_roles = ("CB", "LB", "RB", "CB", "CB", "CM", "RM")
right_roles = ("CB", "CB", "LB", "CB", "CM", "CM", "CM", "LM", "CF")
mixed_left = []
mixed_right = []
for lr in left_roles:
    mixed_left.append(LeftPlayer with role lr, with width 1.5, with length 1.5, in cluster_top_right)

for rr in right_roles:
    mixed_right.append(RightPlayer with role rr, with width 1.5, with length 1.5, in cluster_top_right)

# Ball
ball = Ball right of p1 by 2
