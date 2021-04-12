from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
param game_duration = 600
param deterministic = False
param offsides = False
# ----- Constants -----
init_triangle_length = 35
danger_cone_angle = 70 deg
danger_cone_radius = 20
pass_distance = 10
# ----- Behaviors -----
# ----- Players -----

p1_pos = Point on LeftReg_CM
# spawn p2 to top
p2_pos = Point at p1_pos offset along -30 deg by 0 @ init_triangle_length
# spawn p3 to right
p3_pos = Point at p1_pos offset along -90 deg by 0 @ init_triangle_length
# spawn enemy in between
o1_pos = Point at p1_pos offset along -60 deg by 0 @ init_triangle_length/1.42
p1 = MyPlayer with role "CM", at p1_pos
p2 = MyPlayer with role "CM", at p2_pos
p3 = MyPlayer with role "CM", at p3_pos
ego = MyGK #with behavior IdleBehavior()
#
#
#

o1 = OpPlayer with role "CM", at o1_pos
o2 = OpCF
o3 = OpCB
o0 = OpGK #with behavior IdleBehavior()
#Ball
ball = Ball #ahead of p1 by 2