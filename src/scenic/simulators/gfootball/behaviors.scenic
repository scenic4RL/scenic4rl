from scenic.simulators.gfootball.actions import *
from scenic.simulators.gfootball.model import *
from scenic.core.regions import regionFromShapelyObject
import math

#TODO combine mumtiple behavior

behavior BallRunShoot():
    while True:
        #if not in dbox, run towards it

        pos = self.position

        objects = simulation().objects
        ball = None
        my_team = []
        op_team = []
        for obj in objects:
            if isinstance(obj, Ball):
                ball = obj
            elif isinstance(obj, MyPlayer):
                if obj == self: pass#print("Its Me")
                else: my_team.append(obj)
            elif isinstance(obj, OpPlayer):
                op_team.append(obj)


        #if not active player, take no action

        #if not self.active:
        #    take NoAction()

        #if ball not in my possession run towards it

        x = self.position[0]
        y = self.position[1]
        blx = ball.position[0]
        bly = ball.position[1]

        if self.active:
            print(self.active, self.role, x,y,blx,bly)

        distance = 0
        distance = (((x-blx)*(x-blx)) + (y-bly)*(y-bly))
        distance = math.sqrt(distance)

        direction = 0
        direction = math.atan2(bly-y, blx-x) / math.pi * 180

        if self.active:
            print(self.active, self.role, self.ball_owned, distance, direction)

        if self.active and self.ball_owned:

            # askEddie: how to use penalty_right as defined in model
            if x < 70:
                print("Running towards Goal")
                take SetDirection(5)
            else:
                print("Will shoot now!!")
                take Shoot()

        else:
            print("Will Do Nothing now!!")
            take NoAction()

"""
simulation().timestep
objects = simulation().objects

behavior ShootInDBoxBehavior():
    while True:
        #if in dbox
        # take Shoot()
        #else
        # do nothing
        pass


behavior SlideInRange():
    while True:
        #if ball in close proximity and in control of opposition player
        #   take Slide()

behavior Dribble():
    while True:
        #if ball in my control and opposition player in front of me
        #   take StartDribble()
        #   update dribbling=True # not needed I guess
        #if dribble_Start and opposition player not in front of me
        #   take StopDribble()
        #   update dribbling=True# not needed I guess



"""