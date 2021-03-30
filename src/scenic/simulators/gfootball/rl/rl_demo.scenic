from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 50
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True



# Behaviors
behavior JustShoot2():
    while True:
        print("In Behavior")
        #print("Ball", ball.position)
        #print("P1", p1.position, p1.is_controlled, p1.owns_ball)
        #print("P2", p2.position)
        #print()
        #print()
        #ball = simulation().game_ds.ball
        #my_players = simulation().game_ds.my_players
        #opo_players = simulation().game_ds.op_players
        #game_state = simulation().game_ds.game_state

        print(self.position, self.is_controlled, self.owns_ball)
        if not self.is_controlled:
            take NoAction()
            print("Not controlled -> No Action")
            print()
        else:
            if self.owns_ball:
                take Shoot()
                print("Shoot ")
            else:
                take MoveTowardsPoint(ball.x, ball.y, self.x, self.y)
                print("Move ")

        print("-------------------------------")

# ball at top
ball = Ball at 70 @ 28
ego = MyGK at -99 @ 0
gk = ego
# middle
p2 = MyCB at 70 @ 0
# top with ball
p1 = MyCB at 70 @ 30, with behavior JustShoot2()
OpGK at 99 @ 0
OpCB at 75 @ 30