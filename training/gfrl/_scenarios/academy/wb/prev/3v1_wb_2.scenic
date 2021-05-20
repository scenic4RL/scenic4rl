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
        #if self.is_controlled:
        #    print("---"*80)
        #    print(self)
        #    print()

        take NoAction()
"""
behavior JustShoot():
    while True:
        if self.is_controlled:
            print("---" * 80)
            print(self)
            print()
        take Shoot()
"""

behavior GreedyPlay():
    while True:
        if self.is_controlled:
            print("---" * 80)
            print(self)
            print()

            print("my pos: ", self.x, self.y)
            print("op pos: ", opcb.x, opcb.y)
            print("distance to op: ", (distance from self to opcb))


        dis_pl = distance from self to pl
        dis_pr = distance from self to pr

        dis_gk = distance from self to opgk
        #dis_op = distance from self to opcb


        dest_0 = (85@0)
        dest_1 = (85@10)
        dest_2 = (85@-10)


        if self.x < 75 or abs(self.y)>10:
            x = 80
            y = 0


            if (distance from self to opcb) < 7 and opcb.x>self.x:

                x = Uniform(self.x, x)
                if (distance from self to opcb) < 3:
                    take Dribble()
                    msg = " dribble"
                else:
                    if abs(self.x - opcb.x) > 1:
                        x = self.x

                        if abs(opcb.y) < 5:
                            if opcb.y>0: y = 10
                            else: y = -10
                        else:
                            y = 0

            msg = f"move to {x:0.2f}, {y:0.2f}"
            dir = lookup_direction(x - self.x, y - self.y)
            action = SetDirection(dir)
            # print("moving to ", dir, action)


        else:
            action = Shoot()
            #print("Close Enough, shoot")
            msg = "close enough"

        """
        if (distance from self to right_goal_midpoint) < 25:
            action = Shoot()
            #print("Close Enough, shoot")
            msg = "close enough"
            
        else: 
        
        elif (distance from self to opcb) < 6:
            action = Pass()
            #print("Pass to other")
            msg = "pass other"

        elif (distance from self to dest_1) > 1:

            x = 75
            y = 15
            dir = lookup_direction(x - self.x, y - self.y)
            action = SetDirection(dir)
            #print("moving to ", dir, action)
            msg = "move to dest_1"

        else:
            action = NoAction()
            msg = "No Condition"
        """

        #do MoveToPosition(75, 15)
        #action = MoveToPosition(75, 15)
        #print(action)
        #print(dis_pl, dis_pr, dis_gk, dis_op)
        #take action

        if self.is_controlled:
            print(msg)
            print("Picked Action: ", action)
        take action

        #take Pass()

ego = Ball at 62 @ 0

MyGK at -99 @ 0,  with behavior IdleBehavior()
pm = MyCM at 60 @ 0,  with behavior GreedyPlay()
pl = MyCM at 70 @ 20,  with behavior GreedyPlay()
pr = MyCM at 70 @ -20,  with behavior GreedyPlay()


opgk = OpGK at 99 @ 0
opcb = OpCB at 75 @ 0