from scenic.simulators.gfootball.actions import *
from scenic.simulators.gfootball.actions import ReleaseDirection
from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball import model
from scenic.core.regions import regionFromShapelyObject
import math

from scenic.simulators.gfootball.utilities import *


#model is copied here
from scenic.simulators.gfootball.utilities.constants import ActionCode


def set_dir_if_not(action, sticky_actions):
    is_running = ActionCode.sticky_direction(sticky_actions)
    if not is_running or action.code != is_running:
        return action
    else:
        return NoAction()


behavior IdleBehavior():
    while True:
        take NoAction()

behavior JustShoot():
    while True:
        if not self.is_controlled:
            act = NoAction()
            take act
        else:
            if self.owns_ball:
                take Shoot()
            else:
                take Pass()




behavior JustPass():
    while True:
        take Pass()


behavior RunInCircle():
    while True:
        for i in range(1,9):
            print(i)
            do MoveInDirection(i) for 1 seconds

behavior MoveInDirection(direction_code):
    while True:
        take SetDirection(direction_code)


'''
Move a player to follow the object (e.g. Ball)'s position
'''
behavior FollowObject(object_to_follow, sprint=False, opponent=False):
    while True:
        #ball = simulation().game_ds.ball
        x = object_to_follow.position.x
        y = object_to_follow.position.y
        #print(x,y)

        self_x = self.position.x
        self_y = self.position.y

        distance = math.sqrt(((x-self_x)*(x-self_x)) + (y-self_y)*(y-self_y))

        if opponent:
            corresponding_dir = lookup_direction(self_x-x, self_y-y)
        else:
            corresponding_dir = lookup_direction(x - self_x, y - self_y)

        if distance < 0.5:
            if sprint:
                take ReleaseSprint()
            take ReleaseDirection()
        else:
            take SetDirection(corresponding_dir)
            if sprint:
                take Sprint()
'''
Move a player to position x,y
'''
behavior MoveToPosition(x, y, sprint=False, opponent=False):
    while True:
        #ball = simulation().game_ds.ball

        self_x = self.position.x
        self_y = self.position.y

        distance = math.sqrt(((x-self_x)*(x-self_x)) + (y-self_y)*(y-self_y))

        if opponent:
            corresponding_dir = lookup_direction(self_x - x, self_y - y)
        else:
            corresponding_dir = lookup_direction(x - self_x, y - self_y)

        if distance < 0.5:
            if sprint:
                take ReleaseSprint()
            take ReleaseDirection()
            break
        else:
            take SetDirection(corresponding_dir)
            if sprint:
                take Sprint()

        # print(self.x, self.y, direction, corresponding_dir)

'''
Pass the ball to player.
'''
behavior PassToPlayer(player, pass_type="long"):
    do PassToPoint(player.position.x, player.position.y, pass_type)

behavior PassToPoint(x, y, pass_type="long"):
    assert pass_type in ("long", "short", "high", "shoot")
    if (not self.owns_ball):
        print("Warning: Player don't have ball for passing!")

    self_x = self.position.x
    self_y = self.position.y

    # aim at target player
    # do MoveInDirection(lookup_direction(x - self_x, y - self_y)) for 0.3 seconds
    while self.owns_ball:
        take SetDirection(lookup_direction(x - self_x, y - self_y))

        if pass_type == "shoot":
            take Shoot()
        else:
            take Pass(pass_type)


behavior BuiltinAIBot():
    while True:
        take BuiltinAIAction()



behavior RunRight():
    #is_running = ActionCode.sticky_direction(self.sticky_actions)
    while True:
        take SetDirection(ActionCode.right)

behavior GreedyPlay():
    while True:
        # if not in dbox, run towards it

        pos = self.position
        objects = simulation().objects


        ball = simulation().game_ds.ball
        my_players = simulation().game_ds.my_players
        opo_players = simulation().game_ds.op_players
        game_state = simulation().game_ds.game_state

        act = None
        if not self.controlled:
            act = NoAction()

        dis = distance from self to ball
        angle = math.degrees(angle from self to ball)

        if self.controlled and self.owns_ball:

            dis_to_goal = distance from self to right_goal_midpoint
            dir_angle = math.degrees(angle from self to right_goal_midpoint)
            ang_wrto_x = dir_angle + 90
            if ang_wrto_x>180: ang_wrto_x -= 360
            elif ang_wrto_x < -180: ang_wrto_x += 360

            if dis_to_goal<35 or self in right_pbox:
                sticky_dir = bool(sum(self.sticky_actions[0:8]))
                #if sticky_dir:
                #    act = ReleaseDirection()
                #else:
                act =  Shoot()
            else:
                if ang_wrto_x>45:
                    act = SetDirection(ActionCode.top)
                    act = set_dir_if_not(act, self.sticky_actions)
                elif ang_wrto_x<-45:
                    act = SetDirection(ActionCode.bottom)
                    act = set_dir_if_not(act, self.sticky_actions)
                else:
                    act = SetDirection(ActionCode.right)
                    act = set_dir_if_not(act, self.sticky_actions)

            #print(f"({self.position.x:0.2f}, {self.position.y:0.2f}) {dis_to_goal:0.2f}", dir_angle, ang_wrto_x, act, self.sticky_actions[0:8])


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
                act = set_dir_if_not(act, self.sticky_actions)
            else:
                dir = ActionCode.bottom if disy>0 else ActionCode.top
                act = SetDirection(dir)
                act = set_dir_if_not(act, self.sticky_actions)

            #print(f"{self.position} {ball.position} {dir}")

        assert act is not None
        #print(self.controlled, self.owns_ball, act)
        if self.controlled:

            #print(f"score: {game_state.score} mode: {game_state.game_mode} steps_left: {game_state.steps_left}")
            #print to test Player
            """
            print(f"cntrl: {self.controlled} own: {self.owns_ball} tired: {self.tired_factor:0.4f} yellow: {self.yellow_cards} red: {self.red_card}\n"
                  f"P:({self.position.x:0.2f}, {self.position.y:0.2f}) "
                  f"D:({math.degrees(self.direction):0.2f}) \n"
                  f"V:({self.velocity.x:0.2f}, {self.velocity.y:0.2f})  Speed: {self.speed:0.4f}\n"
                  f"Dis: {dis:0.4f} Angle: {angle:0.2f} Act: {act}")
            """

            """
            print("\n")
            #Print to test Ball
            print(f"Ball: ({ball.position.x:0.2f}, {ball.position.y:0.2f}). dir: {math.degrees(ball.direction):0.2f}\n"
                  f" Heading {math.degrees(ball.heading):0.2f} "
                  f" Speed {ball.speed} "
                  f" Velocity ({ball.velocity.x:0.2f}, {ball.velocity.y:0.2f})"
                  f" Angular Speed {ball.angularSpeed} "
                  f" Owned Team: {ball.owned_team}"
                  )
            """
            #print("")

            #input()
            #print(act)
            #input()
        take act


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
        # take Shoot()no w
        #else
        # do nothing
        pass


behavior SlideInRange():
    while True:
        #if ball in close proximity and in control of opposition player g
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