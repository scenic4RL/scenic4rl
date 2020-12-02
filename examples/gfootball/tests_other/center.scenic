from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from math import degrees

param game_duration = 400
param deterministic = True


ego = MyPlayer at -90@0,
        facing toward center,
        with role "GK"

ball = Ball in right_pbox

p1 = MyPlayer at ((center.x+Range(60,70)) @ (center.y+Range(-30,30))), facing toward ball
p2 = MyPlayer at ((center.x+Range(70,80)) @ (center.y+Range(-30,30))), facing toward ball
p3 = MyPlayer at ((center.x+Range(60,70)) @ (center.y+Range(-30,30))), facing toward ball


OpPlayer at 90@0, with role "GK"


print(ego.position, degrees(ego.heading))
print(p1.position, p1.heading)
print(p2.position, p2.heading)
print(p3.position, p3.heading)
