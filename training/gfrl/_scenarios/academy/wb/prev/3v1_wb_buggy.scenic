from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


behavior IdleBehavior():
    '''
    Always takes NoAction. Note it will not release direction.
    '''
    while True:
        if self.is_controlled:
            print("---"*80)
            print(self)
            print()

        take NoAction()

behavior JustShoot():
    while True:
        if self.is_controlled:
            print("---" * 80)
            print(self)
            print()
        take Shoot()


behavior JustPass():
    while True:
        if self.is_controlled:
            print("---" * 80)
            print(self)
            print()

        dis_pl = distance from self to pl
        dis_pr = distance from self to pr

        dis_gk = distance from self to opgk
        #dis_op = distance from self to opcb

        dest_1 = (75@5)

        print("my pos: ", self.x, self.y)

        if (distance from self to 70@6) < 1:
            action = Pass()

        elif (distance from self to dest_1) > 1:

            x = 75
            y = 15
            dir = lookup_direction(x - self.x, y - self.y)
            action = SetDirection(dir)
            print("moving to ", dir, action)

        else:
            action = NoAction()

        #do MoveToPosition(75, 15)
        #action = MoveToPosition(75, 15)
        #print(action)
        #print(dis_pl, dis_pr, dis_gk, dis_op)
        #take action


        take action

        #take Pass()

ego = Ball at 62 @ 0

MyGK at -99 @ 0,  with behavior IdleBehavior()
pm = MyCM at 60 @ 0,  with behavior JustPass()
pl = MyLM at 70 @ 20,  with behavior IdleBehavior()
pr = MyRM at 70 @ -20,  with behavior IdleBehavior()


opgk = OpGK at 99 @ 0
opcb = OpCB at 75 @ 0