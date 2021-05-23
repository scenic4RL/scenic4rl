from scenic.simulators.gfootball.actions import *
from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball import model
from scenic.core.regions import regionFromShapelyObject, SectorRegion
import math

from scenic.simulators.gfootball.utilities import *


#model is copied here
from scenic.simulators.gfootball.utilities.constants import ActionCode

def aimPointToShoot(player):
    '''
    returns a point at which the player should aim to shoot a goal
    this point is either left or right corner point of the other team's goal
    This aim point is computed with respect to only the nearest opponent
    '''
    if player.team == 'opponent':
        goal_leftside_aimPoint = myTeam_goal_left_corner
        goal_rightside_aimPoint = myTeam_goal_right_corner
    else:
        goal_leftside_aimPoint = opponentTeam_goal_left_corner
        goal_rightside_aimPoint = opponentTeam_goal_right_corner

    opponent = nearestOpponent(player)
    left_radius = distance from player to goal_leftside_aimPoint
    left_heading = angle from player to goal_leftside_aimPoint

    left_shootingSpace = SectorRegion(center=player.position, radius=left_radius, heading=left_heading, angle= 40 deg)

    if not left_shootingSpace.containsPoint(opponent.position):
        print("aim for leftside goal")
        return goal_leftside_aimPoint
    print("aim for rightside goal")
    return goal_rightside_aimPoint


def currentDirectionIndex(player):
    direction = math.degrees(player.heading)
    direction = direction + 360 if direction < 0 else direction % 360
    action_lookup = [3, 4, 5, 6, 7, 8, 1, 2, 3]
    corresponding_dir = action_lookup[round(direction/ 45)]
    return corresponding_dir

def nearestOpponent(player):
    closest_dist = math.inf
    nearestOpponent = None
    for p in simulation().objects:
        distance = distance from player to p
        if distance < closest_dist:
            nearestOpponent = p
            closest_dist = distance
    return nearestOpponent


def set_dir_if_not(action, sticky_actions):
    is_running = ActionCode.sticky_direction(sticky_actions)
    if not is_running or action.code != is_running:
        return action
    else:
        return NoAction()

def opponentInRunway(player, radius=5):
    '''
    checks if there is a different team player in the player's runway
    this runway region is modelled as a half circle centered at the player's position, 
    with radius of 4 meters, in the direction of the player's heading
    '''
    runwayRegion = SectorRegion(center=player.position, radius=radius, heading=player.heading, angle=math.pi/2)
    for p in simulation().objects:
        if isinstance(p, Ball):
            continue
        if player.team is not p.team and runwayRegion.containsPoint(p.position):
            return True
    return False

behavior IdleBehavior():
    '''
    Always takes NoAction. Note it will not release direction.
    '''
    while True:
        take NoAction()

behavior JustShoot():
    '''
    Always tries to Shoot if owns ball, otherwise will Pass.
    '''
    while True:
        if not self.is_controlled:
            take NoAction()
        else:
            if self.owns_ball:
                take Shoot()
            else:
                take Pass()


behavior JustPass():
    '''
    Always try to pass. If not owned ball, will move to the ball.
    '''
    while True:
        take Pass()


behavior RunInCircle(s=1):
    '''
    The agent will run in circle, changing direction every s second.
    '''
    while True:
        for i in range(1,9):
            print(i)
            do MoveInDirection(i) for s seconds

behavior MoveInDirection(direction_code):
    '''
    Always heading to given direction.
    '''
    while True:
        take SetDirection(direction_code)


behavior FollowObject(object_to_follow, terminate_distance=1, sprint=False):
    '''
    Let a player follow the object (e.g. Ball)'s position
    '''
    opponent = self.team == "opponent"
    while True:
        print("following object")
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

        if distance < terminate_distance:
            if sprint:
                take ReleaseSprint()
            take ReleaseDirection()
            break
        else:
            take SetDirection(corresponding_dir)
            if sprint:
                take Sprint()

behavior MoveToPosition(dest_point, sprint=False):
    '''
    Move a player to position x,y. Will Stop if within 1 meter.
    '''
    x = dest_point.x
    y = dest_point.y
    self_x = self.position.x
    self_y = self.position.y
    distance = math.sqrt(((x-self_x)*(x-self_x)) + (y-self_y)*(y-self_y))
    opponent = self.team == "opponent"

    while distance > 1:
        if opponent:
            corresponding_dir = lookup_direction(self_x - x, self_y - y)
        else:
            corresponding_dir = lookup_direction(x - self_x, y - self_y)

        take SetDirection(corresponding_dir)
        if sprint:
            take Sprint()

        self_x = self.position.x
        self_y = self.position.y
        distance = math.sqrt(((x-self_x)*(x-self_x)) + (y-self_y)*(y-self_y))

    if sprint:
        take ReleaseSprint()
    take ReleaseDirection()


# behavior MoveToPosition(destination_point):
#     dist = distance from self to destination_point
#     while dist > 0.5:
#         dest_x = destination_point.x
#         dest_y = destination_point.y
#         self_x = self.position.x
#         self_y = self.position.y
#         take MoveTowardsPoint(dest_x, dest_y, self_x, self_y, opponent= self.team is 'opponent')


behavior PassToPlayer(player, pass_type="long"):
    '''
    Pass the ball to the given player.
    '''
    do PassToPoint(player.position.x, player.position.y, pass_type)

behavior PassToPoint(x, y, pass_type="long"):
    '''
    Pass the ball to the closest player near the point.
    '''
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
    '''
    Always let default AI determine the player's action.
    '''
    while True:
        take BuiltinAIAction()



behavior RunRight():
    '''
    Always runs to the right.
    '''
    #is_running = ActionCode.sticky_direction(self.sticky_actions)
    while True:
        take SetDirection(ActionCode.right)

behavior GreedyPlay():
    '''
    A simple aggressive policy. Will close in and shoot if owns ball, otherwise follow and intercept. 
    '''
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