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