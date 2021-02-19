from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


behavior GetThenPass(target):
    #do BuiltinAIBot() until self.owns_ball
    print("pass")
    do PassToPlayer(target)
    # do MoveToPosition(o0.position.x, o0.position.y)
    do IdleBehavior()

behavior RunForwardAndShoot():
    do MoveToPosition(target_point.x, target_point.y) until self.owns_ball
    print("shoot")
    take Shoot()
    do IdleBehavior()


target_point = Point on right_pbox

ego = MyGK with behavior IdleBehavior()
a1 = MyPlayer with role "CM", on RightReg_LB, with behavior GetThenPass(target_point)
a2 = MyPlayer with role "CF", on RightReg_CB, with behavior RunForwardAndShoot()



o0 = OpGK
#o1 = OpPlayer with role "CB", with behavior MoveToPosition(0,0)

# Ball ahead of a1 by 2
ball = Ball ahead of a1 by 1