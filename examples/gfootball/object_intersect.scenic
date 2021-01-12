from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 100
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??

ego = Ball at 0 @ 0


OpPlayer with role "GK",
         in left_pbox

#xpos_left = Uniform(-30, -20, 10, -10)
#ypos_left = Uniform(-30, 30, 10, -10)
xpos_left = Uniform(-30, -20)
ypos_left = Uniform(-30, 30)


myp2 = MyPlayer with role "GK", offset by xpos_left @ ypos_left
myp3 = MyPlayer with role "CM", offset by xpos_left @ ypos_left

