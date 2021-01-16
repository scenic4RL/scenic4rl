from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False


mygk = MyGK at -10 @  5
mylb = MyLB at -20 @ 10
myrb = MyRB at -30 @ 30

ego = mygk
ball = Ball at 5@5

opgk = OpGK at 90 @ 20
oplb = OpLB at 40 @-30


print(mygk.position)
print(mylb.position)
print(myrb.position)

print(opgk.position)
print(oplb.position)
#print(oprb.position)

