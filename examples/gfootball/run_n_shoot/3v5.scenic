from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 600
param deterministic = False


center = 0 @ 0

ball = Ball at 30@0
ego = ball

mygk = MyPlayer with role "GK",
            right of left_goal_midpoint by 5,
            with behavior BallRunShoot()


myp2 = MyPlayer offset by Uniform(-30, -25, -20) @ Uniform(-30,-20,-10, 0, 10, 20, 30),
            with behavior BallRunShoot()
myp3 = MyPlayer offset by Uniform(-30, -25, -20) @ Uniform(-30,-20,-10, 0, 10, 20, 30),
            with behavior BallRunShoot()

opgk = OpPlayer with role "GK",
                left of right_goal_midpoint by 5
opp1 = OpPlayer offset by Uniform(30, 25, 20) @ Uniform(-30,-20,-10, 0, 10, 20, 30)
opp2 = OpPlayer offset by Uniform(30, 25, 20) @ Uniform(-30,-20,-10, 0, 10, 20, 30)
opp3 = OpPlayer offset by Uniform(30, 25, 20) @ Uniform(-30,-20,-10, 0, 10, 20, 30)
opp4 = OpPlayer offset by Uniform(30, 25, 20) @ Uniform(-30,-20,-10, 0, 10, 20, 30)

