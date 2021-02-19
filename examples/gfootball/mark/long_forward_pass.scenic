from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


behavior GetThenPass(target):
    #do BuiltinAIBot() until self.owns_ball
    print("pass")
    do PassToPlayer(target, "high")
    # do MoveToPosition(o0.position.x, o0.position.y)
    do IdleBehavior()

behavior RunForwardAndShoot():
    do MoveToPosition(target_point.x, target_point.y, True) until self.owns_ball
    print("shoot")
    take Shoot()
    do IdleBehavior()


target_point = Point on RightReg_GK
#require (distance from right_goal_midpoint to target_point) < 10

ego = MyGK with behavior IdleBehavior()

#a2 = MyPlayer with role "CF", on RightReg_LB, facing toward right_goal_midpoint, with behavior RunForwardAndShoot()

a1 = MyPlayer with role "CB", on LeftReg_CF, with behavior GetThenPass(target_point)



o0 = OpGK with behavior IdleBehavior()
#o1 = OpPlayer with role "CB", with behavior MoveToPosition(0,0)


ball = Ball ahead of a1 by 8