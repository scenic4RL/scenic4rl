from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 100
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = Ball at 0 @ 0

MyPlayer with role "GK", in left_pbox
MyPlayer with role "CM", in left_pbox
MyPlayer with role "CM", in left_pbox

OpPlayer with role "GK",
         in left_pbox

xpos_left = Uniform(-30, -20)
ypos_left = Uniform(-30, 30)


myp2 = MyPlayer offset by xpos_left @ ypos_left
myp3 = MyPlayer offset by xpos_left @ ypos_left

