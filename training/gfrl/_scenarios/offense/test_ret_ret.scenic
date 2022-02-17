from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

# ----- Regions -----
attacker_region = get_reg_from_edges(50, 70, 20, -20)

LeftGK with behavior HoldPosition()
RightGK with behavior HoldPosition()


attacker1 = LeftCF on attacker_region
attacker2 = LeftCF on attacker_region
attacker3 = LeftCF on attacker_region

ball = Ball ahead of Uniform(attacker1, attacker2, attacker3) by 2

behavior retrieveBall(ball):
    while True:
        do MoveToPosition(ball.position, reaction_dist=0)

behavior MoveAway():
    do MoveToPosition(90 @ Uniform(-40, 40))
    do HoldPosition()

ego = RightCB on right_penaltyBox, with behavior retrieveBall(ball)
RightCB on right_penaltyBox, with behavior retrieveBall(ball)