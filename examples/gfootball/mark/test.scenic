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
behavior DribbleWhenClose(enemy):
    while True:
        if (distance from self to enemy) < 9:
            take Dribble()
        take SetDirection(5) #right



    do BuiltinAIBot()



# ----- Players -----

ego = MyGK with behavior IdleBehavior()

p1_pos = Point on LeftReg_CM
o1_pos = Point at p1_pos offset along -90 deg by 0 @ 20


#Ball
ball = Ball ahead of p1_pos by 1

o1 = OpPlayer with role "CM", at o1_pos, with behavior FollowObject(ball)
p1 = MyPlayer with role "CM", at p1_pos, with behavior DribbleWhenClose(o1)
o0 = OpGK with behavior IdleBehavior()


