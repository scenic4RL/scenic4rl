from scenic.simulators.gfootball.actions import *
from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball import model
from scenic.core.regions import regionFromShapelyObject
import math

from scenic.simulators.gfootball.utilities import *
#TODO combine mumtiple behavior

#model is copied here
from scenic.simulators.gfootball.utilities.constants import ActionCode

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
                if obj == self: pass #print("Its Me")
                else: my_team.append(obj)
            elif isinstance(obj, OpPlayer):
                op_team.append(obj)


        #if not active player, take no action

        #if not self.active:
        #    take NoAction()

        #if ball not in my possession run towards it

        x = self.position.x
        y = self.position.y
        blx = ball.position.x
        bly = ball.position.y

        if self.active:
            print(self.active, self.role, x,y,blx,bly)

        distance = 0
        distance = (((x-blx)*(x-blx)) + (y-bly)*(y-bly))
        distance = math.sqrt(distance)

        direction = 0
        direction = math.atan2(bly-y, blx-x) / math.pi * 180

        #if self.active:
        #    print(self.active, self.role, self.ball_owned, distance, direction)

        if self.active and self.ball_owned:

            # askEddie: how to use penalty_right as defined in model
            #if self.position in model.penalty_right:
            if self.position.x >= 59:
                print("Will shoot now!!")
                take Shoot()
            else:
                print("Running towards Goal")
                take SetDirection(ActionCode.right)



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