from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = True



mygk = MyPlayer in left_pbox,
        with role "GK",
        with behavior RandomKick

ego = mygk

ball = Ball at 0@0

myp0 = MyPlayer at -10 @ -10,
        with role "LB",
        with behavior RandomKick

myp1 = MyPlayer at -10 @ 10,
        with role "CB",
        with behavior RandomKick

opgk = OpPlayer in right_pbox,
        with role "GK"

op1 = OpPlayer at 15 @ 0,
        with role "CB"
"""
op2 = OpPlayer at 15 @ 10,
        with role "RB"

op2 = OpPlayer at 15 @ -10,
        with role "LB"
"""