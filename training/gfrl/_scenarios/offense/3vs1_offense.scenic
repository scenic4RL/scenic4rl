from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# ---- behaviors ----
behavior goToMidPoint():
    print("1")
    ds = simulation().game_ds
    opponent_list = ds.left_players
    # player_owns_ball = player_with_ball(ds, ball, team=1)
    player_owns_ball = None

    while True:
        for o in opponent_list:
            if (distance from o to ball) < 2:
                player_owns_ball = o
                # print("Got player owns ball")
                break
        closest_opp_to_self, closest_opp_to_self_distance = get_closest_player_info(self, opponent_list)
        closest_opp_to_owner, closest_opp_to_owner_distance = get_closest_player_info(player_owns_ball, opponent_list)
        mid_x = (closest_opp_to_self.x + closest_opp_to_owner.x) / 2
        mid_y = (closest_opp_to_self.y + closest_opp_to_owner.y) / 2
        # print("Got the midpoint of the opponent closest to the ball owner and the opponent closest to self")

        mid_x_range = mid_x + Range(-5,5)
        mid_y_range = mid_y + Range(-5,5)
        do MoveToPosition(mid_x_range @ mid_y_range)
        # print("Moving to midpoint")
        if (distance from self to ball) < 2:
            do dribbleToAndShoot(Point on opponent_goal)
            # print("Dribbled")
            break
    do HoldPosition()

behavior helpGK():
    print("2")
    goal_position = Point on o0_spawn
    # print(goal_position.x)
    # print(goal_position.y)
    # print(o0.x)
    # print(o0.y)
    while True:
        take MoveTowardsPoint(goal_position, self.position, True)
        if (distance from o0 to self) < 5:
            break
    while True:
        if self.owns_ball:
            do dribbleToAndShoot(Point on opponent_goal)
        else:
            take MoveTowardsPoint(ball.position, self.position, rightTeam=True)


# ---- behaviors 2 ----
behavior FollowObj(obj):
    print("3")
    while True:
        if self.owns_ball:
            take NoAction()
        else:
            take MoveTowardsPoint(obj.position, self.position, rightTeam=True)

behavior FollowPersonWithBall(ball):
    print("4")
    ds = simulation().game_ds

    while True:
        p = player_with_ball(ds, ball, team=1)
        if p is self or p is  None:
            take NoAction()
        else:
            take MoveTowardsPoint(p.position, self.position, rightTeam=True)

# ----- Regions -----

# for offside rule
p1_spawn = get_reg_from_edges(230, 30, 10, -10)
o0_spawn = get_reg_from_edges(100, 98, 2, -2)
opponent_goal = get_reg_from_edges(-100, -98, 2, -2)
# ----- Players -----
# Left
ego = LeftGK with behavior HoldPosition(), on opponent_goal

p1 = LeftPlayer with role "AM", on p1_spawn
p3 = LeftPlayer with role "AM", right of p1 by 20
p2 = LeftPlayer with role "AM", ahead of p1 by 20

# Right
o0 = RightGK on o0_spawn
o1 = RightPlayer right of p2 by 20, behavior Uniform(goToMidPoint(),helpGK(),FollowObj(ball),FollowPersonWithBall(ball))

# Ball
ball = Ball ahead of p1 by 2