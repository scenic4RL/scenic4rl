from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

behavior RunThenShoot():
    #game_ds = simulation().game_ds

    while True:
        #print("In Behavior")
        #print(self.position, self.is_controlled, self.owns_ball, "ball", ball.x, ball.y)
        if not self.is_controlled:
            take NoAction()
            #print("Not controlled -> No Action")
            #print()
        else:
            if self.owns_ball:
                if self.x <10:
                    #print("Sprint On ")
                    take Sprint()

                    act = MoveTowardsPoint(80, 0, self.x, self.y)
                    # act = self.MoveToPosition(80, 0, True)
                    #print("Move with ball: ", act.code)
                    take act

                if self.x < 75:
                    act = MoveTowardsPoint(80, 0, self.x, self.y)
                    #act = self.MoveToPosition(80, 0, True)
                    #print("Move with ball: ", act.code)
                    take act

                elif 75 < self.x < 80:
                    #print("release Sprint")
                    take ReleaseSprint()

                else:
                    #print("Shoot ")
                    take Shoot()

            else:
                act = MoveTowardsPoint(ball.x, ball.y, self.x, self.y)
                #print("Move to ball", act)
                take act
                #print("Move ")

            take NoAction()

ball = Ball at 2 @ 0
ego = ball

MyGK at -98 @ 0, with behavior RunThenShoot()
MyCB at 0 @ 0, with behavior RunThenShoot()


OpGK at -98 @ -41
OpLB at -22 @ -20
OpCB at -22 @ -10
OpCM at -22 @ 0
OpCB at -22 @ 10
OpRB at -22 @ 20