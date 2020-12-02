from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


#how to specify that if there is one/ more than one player on one side, there must be one GK??
#ego = LeftGoalMidPoint

ego = MyPlayer at -90 @ 0,
            facing 270 deg,
            with role "GK"


ball = Ball left of ego #should be placed at (-90,10)?

"""
mp1 = MyPlayer at -90 @ 0,
            facing 0deg,
            with role "GK"
MyPlayer with role "GK", left of b by 10
OpPlayer with role "GK", right of b by 10
"""
import math
print(f"My Player: ", ego.position, math.degrees(ego.heading))
print("Ball: ", ball.position, math.degrees(ball.heading))