from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False


behavior RunThenReceive():
    print(target_pt.x, target_pt.y)

    print("Now start running")
    do MoveToPosition(target_pt.x, target_pt.y, True) until self.owns_ball
    print("received ball")

    do BuiltinAIBot()


behavior WaitThenPass():
    do IdleBehavior() until (self.owns_ball and (distance from a2 to target_pt) < 2)
    print("pass")
    do PassToPlayer(a1, "long")
    do IdleBehavior()

ego = MyGK with behavior IdleBehavior()

a1_pos = Point on LeftReg_CM
# spawn enemy to the right
o1_pos = Point at a1_pos offset along -90 deg by 0 @ 15
# spawn p2 further behind
a2_pos = Point at o1_pos offset along -90 deg by 0 @ 15
# target point at 45 deg
target_pt = Point at a1_pos offset along -45 deg by 0 @ 30



a1 = MyPlayer with role "CM", facing toward right_goal_midpoint, at a1_pos, with behavior WaitThenPass()
a2 = MyPlayer with role "CM", at a2_pos, with behavior RunThenReceive()

# TODO: add enemy o1 when the freeze bug is fixed
o0 = OpGK with behavior IdleBehavior()

#Ball
ball = Ball ahead of a1 by 3