from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 600
param deterministic = False


behavior JustPass():
    do MoveToPosition(a2.position.x, a2.position.y) until (distance from self to a2) < 60 and self.owns_ball
    print("pass")
    do PassToPlayer(a2)
    print("pass done")

    # do IdleBehavior()
    do MoveToPosition(o0.position.x, o0.position.y)


ego = MyGK with behavior IdleBehavior()
a1 = MyCB with behavior JustPass()
a2 = MyLB with behavior IdleBehavior()


o0 = OpGK
Ball ahead of a1 by 3