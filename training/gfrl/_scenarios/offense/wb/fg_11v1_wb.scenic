from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from scenic.simulators.gfootball.behaviors import *

param game_duration = 200
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

verbose = False
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

behavior GreedyRS():
    '''
    Always takes NoAction. Note it will not release direction.
    '''
    while True:
        #if self.is_controlled:
        #    print("---"*80)
        #    print(self)
        #    print()

        if self.x < 75 or abs(self.y)>10:
            x = 80
            y = 0

            if (distance from self to opgk) < 7:

                act =  Shoot()
                msg = " shoot"

            else:

                msg = f"move to {x:0.2f}, {y:0.2f}"
                dir = lookup_direction(x - self.x, y - self.y)
                action = SetDirection(dir)

        else:
            action = Shoot()
            #print("Close Enough, shoot")
            msg = "close enough"

        if self.is_controlled and verbose:

            print(msg)
            print("Picked Action: ", action)
            print("*"*80)
            print()

        take action

ego = Ball at 0 @ 0

LeftGK at -98 @ 0, with behavior GreedyRS()
LeftLB at -60 @  30, with behavior GreedyRS()
LeftCB at -70 @  12, with behavior GreedyRS()
LeftCB at -70 @ -12, with behavior GreedyRS()
LeftRB at -60 @ -30, with behavior GreedyRS()
LeftLM at -25 @  15, with behavior GreedyRS()
LeftCM at -50 @  10, with behavior GreedyRS()
LeftCM at -50 @ -10, with behavior GreedyRS()
LeftRM at -25 @ -15, with behavior GreedyRS()
LeftAM at -15 @ -2, with behavior GreedyRS()
LeftCF at  -2 @ -1, with behavior GreedyRS()

opgk = RightGK
