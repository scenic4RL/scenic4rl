from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False


mygk = MyGK at -90 @ 0
mylb = MyLB at -40@-10
myrb = MyRB at -40@10

ego = mygk
ball = Ball at 0@0

opgk = OpGK at 90 @ 0
oplb = OpLB at 40@10
#oprb = OpRB at 40@-10


print(mygk.position)
print(mylb.position)
print(myrb.position)

print(opgk.position)
print(oplb.position)
#print(oprb.position)

