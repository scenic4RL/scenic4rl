from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
import math

param game_duration = 600
param deterministic = False

# ----- Constants -----
danger_cone_angle = 30 deg
danger_cone_radius = 30

pass_distance = 5

# ----- Behaviors -----
behavior SlideAndRun():
    do FollowObject(ball) until (distance from self to ball) < 9
    while not self.owns_ball:
        take MoveTowardsPoint(ball.position.x, ball.position.y, self.position.x, self.position.y)
        take Slide()
        break


    do FollowObject(ball) until self.owns_ball
    do BuiltinAIBot()



# ----- Players -----

ego = MyGK with behavior IdleBehavior()

p1_pos = Point on LeftReg_CM
o1_pos = Point at p1_pos offset along -90 deg by 0 @ 20


# , facing toward right_goal_midpoint
p1 = MyPlayer with role "CM", at p1_pos, with behavior SlideAndRun()

o1 = OpPlayer with role "CM", at o1_pos, with behavior FollowObject(ego)
o0 = OpGK with behavior IdleBehavior()

#Ball
ball = Ball ahead of o1 by 1
