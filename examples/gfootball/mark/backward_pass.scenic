from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


behavior GetThenPass(target_player):
    #do BuiltinAIBot() until self.owns_ball
    do RunInCircle() until self.owns_ball
    print("pass")
    do PassToPlayer(target_player)
    # do MoveToPosition(o0.position.x, o0.position.y)
    do IdleBehavior()



ego = MyGK with behavior IdleBehavior()
#a1 = MyPlayer with role "CB", with behavior MoveInDirection(5)
a1 = MyCB with behavior GetThenPass(ego)
a2 = MyCMM with behavior GetThenPass(a1)

o0 = OpGK
#o1 = OpPlayer with role "CB", with behavior MoveToPosition(0,0)

# Ball ahead of a1 by 2
ball = Ball ahead of a2 by 2