from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


behavior GetThenPass(target):
    do IdleBehavior() until (self.owns_ball and (distance from a2 to target_point) < 15)
    do PassToPoint(target.x, target.y, "high")
    print("finish passing")
    # do MoveToPosition(o0.position.x, o0.position.y)
    do IdleBehavior()

behavior RunForwardAndShoot():
    do MoveToPosition(target_point.x, target_point.y, True) until self.owns_ball
    while self.owns_ball:
        take Shoot()
        print("shoot")
    do BuiltinAIBot()

behavior CatchOrTerminate():
    print(self.heading)
    try:
        do IdleBehavior()
    interrupt when self.owns_ball:
        print(self.heading)
        do BuiltinAIBot() for 2 seconds
        terminate

target_cone = SectorRegion(right_goal_midpoint, 40, 90 deg, 60 deg) # 90 deg=left
target_point = Point on target_cone
require (distance from target_point to right_goal_midpoint) > 20

ego = MyGK with behavior IdleBehavior()

a2 = MyPlayer with role "CF", on Uniform(RightReg_LB, RightReg_RB, RightReg_CB), facing toward target_point, with behavior RunForwardAndShoot()

a1 = MyPlayer with role "CB", on Uniform(LeftReg_CF, LeftReg_LM, LeftReg_RM), facing toward right_goal_midpoint, with behavior GetThenPass(target_point)



o0 = OpGK facing toward left_goal_midpoint, with behavior CatchOrTerminate()
#o1 = OpPlayer with role "CB", with behavior MoveToPosition(0,0)


# ball = Ball ahead of a1 by 8
ball = Ball ahead of a1 by 15
