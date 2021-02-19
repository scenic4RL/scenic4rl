from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False


behavior PassRunReceive():
    print(target_point.x, target_point.y)

    do PassToPlayer(a2, "short")
    print("first pass. Now start running")
    do MoveToPosition(target_point.x, target_point.y, True) until (self.owns_ball and (distance from self to target_point)<2)
    print("received ball")

    do BuiltinAIBot()


behavior WaitThenPass():
    do IdleBehavior() until (self.owns_ball and (distance from a1 to target_point) < 2)
    print("pass back")
    do PassToPlayer(a1, "short")
    do BuiltinAIBot()

ego = MyGK with behavior IdleBehavior()

a1_pos = Point on LeftReg_CM
view_cone = SectorRegion(a1_pos, 50, -1.59, 40 deg) # center, radius, heading, angle

a2_pos = Point at Range(10, 15) @ Range(10, 15) relative to a1_pos
require(not a2_pos in view_cone)

target_point = Point at Range(20, 25) @ Range(-15, -10) relative to a1_pos
require(not target_point in view_cone)


a1 = MyPlayer with role "CM", facing toward right_goal_midpoint, at a1_pos, with behavior PassRunReceive()
a2 = MyPlayer with role "CM", at a2_pos, with behavior WaitThenPass()

# TODO: add enemy when the freeze bug is fixed
#o1 = OpPlayer with role "CF", ahead of a1 by 10, with behavior IdleBehavior()
o0 = OpGK with behavior IdleBehavior()

#Ball
ball = Ball ahead of a1 by 3