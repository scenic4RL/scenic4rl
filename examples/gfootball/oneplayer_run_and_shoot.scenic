from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball import model
#1500 is 45 minutes
param real_time = False
param game_duration = 500
param deterministic = False

#AskEddie: What is the significance of ego

#how to specify that if there is one/ more than one player on one side, there must be one GK??


#in gfootball the applied actions correspond to the active player (player with ball / closest to ball), but scenic applies behavior to each and every object
ego = MyPlayer on penalty_left,
                with role "GK",
                with behavior BallRunShoot()

#askEddie
ball = Ball at -10 @ 10
#ball = Ball at 20 @ 20

MyPlayer with behavior BallRunShoot()#left of ego by 5

"""
MyPlayer at -50 @ 25,
         with role "CB",
         with behavior BallRunShoot()

MyPlayer with role "CM",
         with behavior BallRunShoot()
"""

#AskEddie how to define constants
OpPlayer with role "GK"
        #on penalty_right

#OpPlayer at -50 @ 25,
#         with role "CB"

