from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
# from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True
# Constants
danger_cone_angle = 70 deg
danger_cone_radius = 20
# Behaviors
behavior JustShoot():
    while True:
        if self.owns_ball:
            #take ReleaseDirection()
            if (distance from self to right_goal_midpoint) < 30:
                take Shoot()
                #print("shoot")
            else:
                take MoveTowardsPoint(right_goal_midpoint.x, right_goal_midpoint.y, self.x, self.y)
            #do MoveToPosition(right_goal_midpoint.x, right_goal_midpoint.y) until (distance from self to right_goal_midpoint) < 35
            #take SetDirection(6)
            #take Shoot()
        else:
            # take SetDirection(5)
            take ReleaseDirection()
# behavior PassThenShoot():
#     ds = simulation().game_ds
#     while True:
#         if not self.is_controlled:
#             take NoAction()
#             #print("Not controlled")
#         else:
#             if self.owns_ball:
#                 if 50 deg < (angle from right_goal_midpoint to self) < 140 deg:
#                     close_point = Point at right_goal_midpoint offset along 135 deg by 0 @ Range(10,15)
#                     take Dribble()
#                     do MoveToPosition(close_point.x, close_point.y) until ((distance from self to close_point) < 5) or (get_closest_player_dis(self.position, ds.op_players)[1] < 8)
#                     print("closed in")
#                     take Shoot()
#                     take ReleaseDribble()
#                     print("Shoot")
#                 else:
#
#                     # pass to a player
#                     danger_cone = SectorRegion(self, danger_cone_radius, self.heading, danger_cone_angle)
#                     safe_players = [p for p in simulation().game_ds.my_players if p not in danger_cone]
#                     print("pass")
#                     do PassToPlayer(get_closest_player_dis(self.position, safe_players)[0], "short")
#                     take NoAction()
#
#             else:
#                 take MoveTowardsPoint(ball.x, ball.y, self.x, self.y)
#                 #print("Move")
behavior RunThenShoot():
    while True:
        # print("p1: ", p1.position, p1.is_controlled, p1.owns_ball)
        # print("p2: ", p2.position, p2.is_controlled, p2.owns_ball)
        # print("gk: ", gk.position, gk.is_controlled, gk.owns_ball)
        if not self.is_controlled:
            take NoAction()
            print("Not controlled")
        else:
            if self.owns_ball:
                close_point = Point at right_goal_midpoint offset along 45 deg by Range(-3,3) @ Range(20,40)
                if (distance from self to close_point) < 3:
                    print("Shoot")
                    take Shoot()
                else:
                    take MoveTowardsPoint(close_point.x, close_point.y, self.x, self.y)
                    take Sprint()
                    print("Closing in")
            else:
                take MoveTowardsPoint(ball.x, ball.y, self.x, self.y)
                print("Move", self.owns_ball)
behavior JustPass():
    passed = False
    while True:
        if passed:
            take SetDirection(5)
            if not self.owns_ball:
                passed = False
        else:
            if self.owns_ball:
                #print("pass!!!")
                # do PassToPlayer(p2, "short")
                take Pass()
                take SetDirection(5)
                passed = True
            else:
                take MoveTowardsPoint(ball.x, ball.y, self.x, self.y)
# ball at top
ball = Ball at 70 @ 28
ego = MyGK at -99 @ 0,  with behavior JustShoot()
gk = ego
# P2 Turing
p2 = MyCF at 70 @ 0, with behavior JustShoot()
# P1 top with ball
p1 = MyCB at 70 @ 30, with behavior JustPass()
OpGK at 99 @ 0
OpCB at 75 @ 30