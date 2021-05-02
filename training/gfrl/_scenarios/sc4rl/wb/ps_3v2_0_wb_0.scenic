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


behavior GreedyPlay():
    '''
    Always takes NoAction. Note it will not release direction.
    '''
    import random

    dest_1 = 80 @ 0
    dest_2 = 80 @ random.randint(8,12)
    dest_3 = 80 @ -10

    #dest_ys = [y + random.random() * random.choice([-1, 1]) for y in range(-10, 10 + 1, 2)]
    #dests = [dest_1, dest_2, dest_3]
    dests = [dest_2]

    x_lim = random.randint(75, 77)
    pass_ts = random.randint(7,8)

    passed = False

    while True:

        msg = ""

        if not self.is_controlled:
            action = NoAction()
            take action


        elif not self.owns_ball:

            #if (distance from self to ball) < 5 and ball.speed<0.01:

            """
            if self.x > 75 and abs(self.y) < 15:
                action = Shoot()
                if self.is_controlled and verbose: print(f"{action} doesnt own ball")
                take action
            else:
            """
            passed = False
            dir = lookup_direction(ball.x - self.x, ball.y - self.y)
            current_dir = dir
            action = SetDirection(dir)
            if self.is_controlled and verbose: print(f"{action} doesnt own ball")
            take action
            #else:
            #    action = NoAction()
            #    msg += " no action - wait for ball"

        else:

            if self.x > x_lim and abs(self.y) < 10:


                for _ in range(1):
                    sel_dest = (99 @ -5)
                    dir = lookup_direction(sel_dest.x - self.x, sel_dest.y - self.y)
                    action = SetDirection(dir)
                    if verbose: print("take ", action, " ")
                    take action

                """
                for _ in range(1):
                    action = NoAction()
                    if verbose: print("take ", action, " ")
                    take action
                
                
                for _ in range(1):
                    sel_dest = (99 @ -5)
                    dir = lookup_direction(sel_dest.x - self.x, sel_dest.y - self.y)
                    msg += f" move to {sel_dest.x}, {sel_dest.y}"

                    action = SetDirection(dir)
                    if verbose: print("take ", action, " ")
                    take action
                
                    #sel_dest = (99 @ -5)
                    #dir = lookup_direction(sel_dest.x - self.x, sel_dest.y - self.y)
                    #msg += f" move to {sel_dest.x}, {sel_dest.y}"

                    #action = SetDirection(dir)
                    #if verbose: print("take ", action, " ")
                    #take action
                """
                if self.is_controlled and verbose: print("shoot")
                action = Shoot()
                take action

            else:

                step = 0.5

                min_ds = 100
                sel_dest = dests[0]
                for dest in dests:

                    dx = (dest.x - self.x)
                    if abs(dx)>step: dx = step if dx>0 else -1*step
                    else: dx = 0

                    dy = (dest.y - self.y)
                    if abs(dy)>step: dy = step if dy>0 else -1*step
                    else: dy = 0

                    new_x = self.x + dx
                    new_y = self.y + dy

                    opds = (distance from (new_x@new_y) to opcb)
                    #print(opds)
                    if opds<min_ds:
                        min_ds = opds
                        sel_dest = dest


                if min_ds < pass_ts and opcb.x > self.x:
                    if passed:
                        if self.is_controlled and verbose: print("noaction")
                        take NoAction()
                    else:
                        if self.is_controlled and verbose: print("pass")
                        action = Pass()
                        take action
                        passed = True


                else:
                    dir = lookup_direction(sel_dest.x - self.x, sel_dest.y - self.y)

                    action = SetDirection(dir)
                    if self.is_controlled and verbose: print(
                        f" set direction {action} move to {sel_dest.x}, {sel_dest.y}")
                    take action
                        #msg += f" move to {sel_dest.x}, {sel_dest.y}"



        """
        if self.is_controlled and verbose:
            print("In Greedy Play")
            print(msg)
            print("Picked Action: ", action)
            print("*"*80)
            print()
        
        take action
        """


ball = Ball at 52 @ 0
ego = ball

mygk = MyGK at -98 @  0, with behavior GreedyPlay()
myam = MyAM at 50 @  0, with behavior GreedyPlay()
mycf = MyCF at 80 @ -10, with behavior GreedyPlay()

opgk = OpGK at  98 @   0
opcb = OpCB at  70 @  -5

