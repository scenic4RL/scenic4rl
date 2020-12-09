from scenic.simulators.gfootball.actions import *
from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball import model
from scenic.core.regions import regionFromShapelyObject
import math

from scenic.simulators.gfootball.utilities import *
#TODO combine mumtiple behavior

#model is copied here
from scenic.simulators.gfootball.utilities.constants import ActionCode

behavior RandomKick():
    while True:
        # if not in dbox, run towards it

        pos = self.position
        objects = simulation().objects


        ball = simulation().ball
        my_players = simulation().my_players
        opo_players = simulation().opo_players

        act = None
        if not self.controlled:
            act = NoAction()

        dis = distance from self to ball
        angle = math.degrees(angle from self to ball)

        if self.controlled and self.owns_ball:

            if self in right_pbox:
                act =  Shoot()
            else:
                act = SetDirection(ActionCode.right)

        elif self.controlled and not self.owns_ball:


            #print(dis)
            disx = self.x - ball.x
            disy = self.y - ball.y

            #if close tackle
            if dis < 1.5:
                act = Sliding()
            elif math.fabs(disx) > math.fabs(disy):
                dir = ActionCode.left if disx>0 else ActionCode.right
                act =  SetDirection(dir)
            else:
                dir = ActionCode.bottom if disy>0 else ActionCode.top
                act = SetDirection(dir)

            #print(f"{self.position} {ball.position} {dir}")

        assert act is not None
        #print(self.controlled, self.owns_ball, act)
        if self.controlled:
            #print to test Player

            """
            values['position'] = obj.position
			values['direction'] = obj.direction
			values['tired_factor'] = obj.tired_factor
			values['yellow_cards'] = obj.yellow_cards
			values['red_card'] = obj.yellow_cards
			values['role'] = obj.role

			values['sticky_actions'] = obj.sticky_actions


			values['velocity'] = 0
			values['angularSpeed'] = obj.angularSpeed
			values['speed'] = 0
			values['heading'] = 0
            """
            print(f"cntrl: {self.controlled} own: {self.owns_ball} "
                  f"P:({self.position.x:0.2f}, {self.position.y:0.2f}) "
                  f"D:({math.degrees(self.direction):0.2f}) "
                  f"Dis: {dis:0.4f} Angle: {angle:0.2f} Act: {act}")


            """
            #Print to test Ball
            print(f"Ball: ({ball.position.x:0.2f}, {ball.position.y:0.2f}). dir: {math.degrees(ball.direction):0.2f}\n"
                  f" Heading {math.degrees(ball.heading):0.2f} "
                  f" Speed {ball.speed} "
                  f" Velocity ({ball.velocity.x:0.2f}, {ball.velocity.y:0.2f})"
                  f" Angular Speed {ball.angularSpeed} "
                  f" Owned Team: {ball.owned_team}"
                  ) 
            """

            input()
        take act

behavior GreedyPlay():
    while True:
        #if not in dbox, run towards it

        pos = self.position
        objects = simulation().objects

        ball = simulation().ball
        my_players = simulation().my_players
        opo_players = simulation().opo_players


        #print(f"Ball")
        """
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
        """

        x = self.position.x
        y = self.position.y
        blx = ball.position.x
        bly = ball.position.y



        #if self.active:
        #    print(self.active, self.role, self.ball_owned, distance, direction)

        if self.controlled and self.owns_ball:
            if self.position in right_pbox:
                #print("Will shoot now!!")
                take Shoot()
            else:
                #print("Running towards Goal")
                take SetDirection(ActionCode.right)



        else:
            #print("Will Do Nothing now!!")
            take NoAction()


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

        #if self.active:
        #    print(self.active, self.role, x,y,blx,bly)

        distance = 0
        distance = (((x-blx)*(x-blx)) + (y-bly)*(y-bly))
        distance = math.sqrt(distance)

        direction = 0
        direction = math.atan2(bly-y, blx-x) / math.pi * 180

        #if self.active:
        #    print(self.active, self.role, self.ball_owned, distance, direction)

        if self.controlled and self.owns_ball:

            # askEddie: how to use penalty_right as defined in model
            #if self.position in model.penalty_right:
            if self.position in pbox_right:
                #print("Will shoot now!!")
                take Shoot()
            else:
                #print("Running towards Goal")
                take SetDirection(ActionCode.right)


        else:
           #print("Will Do Nothing now!!")
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