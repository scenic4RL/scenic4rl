from scenic.simulators.gfootball.actions import *
from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball import model
from scenic.core.regions import regionFromShapelyObject, SectorRegion
import math

from scenic.simulators.gfootball.utilities import *


#model is copied here
from scenic.simulators.gfootball.utilities.constants import ActionCode

def aimPointToShoot(player, angle = 30 deg):
    '''
    returns a point at which the player should aim to shoot a goal
    this point is either left or right corner point of the other team's goal
    This aim point is computed with respect to only the nearest opponent
    '''
    if player.team == 'right':
        goal_leftside_aimPoint = left_goal_left_corner
        goal_rightside_aimPoint = left_goal_right_corner
    else:
        goal_leftside_aimPoint = right_goal_left_corner
        goal_rightside_aimPoint = right_goal_right_corner

    opponent = nearestOpponent(player)
    left_radius = distance from player to goal_leftside_aimPoint
    left_heading = angle from player to goal_leftside_aimPoint
    left_shootingSpace = SectorRegion(center=player.position, radius=left_radius, heading=left_heading, angle= angle)
    left_goalside_is_open = not left_shootingSpace.containsPoint(opponent.position)

    right_radius = distance from player to goal_rightside_aimPoint
    right_heading = angle from player to goal_rightside_aimPoint
    right_shootingSpace = SectorRegion(center=player.position, radius=right_radius, heading=right_heading, angle= angle)
    right_goalside_is_open = not right_shootingSpace.containsPoint(opponent.position)

    #print("left_goalside_is_open: ", left_goalside_is_open)
    #print("right_goalside_is_open: ", right_goalside_is_open)
    #print("left_heading: ", left_heading)
    #print("right_heading: ", right_heading)
    #print("return")

    if left_goalside_is_open and right_goalside_is_open:
        return Uniform(goal_leftside_aimPoint, goal_rightside_aimPoint)
    elif not left_goalside_is_open and right_goalside_is_open:
        return goal_rightside_aimPoint
    elif left_goalside_is_open and not right_goalside_is_open:
        return goal_leftside_aimPoint
    else: 
        return None
    return None


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
        if not isinstance(p, Ball) and p.team != player.team and distance < closest_dist:
            nearestOpponent = p
            closest_dist = distance
    return nearestOpponent

def nearestTeammate(player):
    closest_dist = math.inf
    nearestTeammate = None
    for p in simulation().objects:
        distance = distance from player to p
        if not isinstance(p, Ball) and p.team == player.team and distance < closest_dist:
            nearestTeammate = p
            closest_dist = distance
    return nearestTeammate

def teammateHasBallPossession(player):
    ''' this includes case when the player itself has the ball possession '''
    for p in simulation().objects:
        if not isinstance(p, Ball) and p.team == player.team and p.owns_ball:
            return True
    return False

def opponentTeamHasBallPossession(player):
    ''' this includes case when the player itself has the ball possession '''
    for p in simulation().objects:
        if not isinstance(p, Ball) and p.team != player.team and p.owns_ball:
            return True
    return False

def set_dir_if_not(action, sticky_actions):
    is_running = ActionCode.sticky_direction(sticky_actions)
    if not is_running or action.code != is_running:
        return action
    else:
        return NoAction()

def opponentInRunway(player, reactionDistance=5):
    '''
    checks if there is a different team player in the player's runway
    this runway region is modelled as a half circle centered at the player's position, 
    with radius of 4 meters, in the direction of the player's heading
    '''
    radius = reactionDistance
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

behavior MoveToPosition(dest_point, sprint=False):
    '''
    Move a player to position x,y. Will Stop if within 2 meter 
    '''
    x = dest_point.x
    y = dest_point.y
    self_x = self.position.x
    self_y = self.position.y
    distance = math.sqrt(((x-self_x)*(x-self_x)) + (y-self_y)*(y-self_y))
    withinDistanceFromDestPt = 10 if sprint else 2

    while distance > withinDistanceFromDestPt:
        if self.team == 'right':
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


behavior ShortPassTo(player):
    '''
    Always try to pass. If not owned ball, will move to the ball.
    '''
    is_player_rightTeam = self.team == "right"
    take MoveTowardsPoint(player.position, self.position, is_player_rightTeam)
    take Pass("short")
    take ReleaseSprint()
    take ReleaseDirection()


behavior HighPassTo(player):
    '''
    Always try to pass. If not owned ball, will move to the ball.
    '''
    is_player_rightTeam = self.team == "right"
    take MoveTowardsPoint(player.position, self.position, is_player_rightTeam)
    take Pass("high")
    take ReleaseSprint()
    take ReleaseDirection()

behavior LongPassTo(player):
    '''
    Always try to pass. If not owned ball, will move to the ball.
    '''
    is_player_rightTeam = self.team == "right"
    take MoveTowardsPoint(player.position, self.position, is_player_rightTeam)
    take Pass("long")
    take ReleaseSprint()
    take ReleaseDirection()

behavior HoldPosition():
    while True:
        take ReleaseSprint()
        take ReleaseDirection()

def nearestOpponentRelativePositionAhead(player):
    ''' for the given player, this function returns which side its nearest opponent is 
    with respect to the player's heading direction. If there is no nearest opponent in
    the player's heading direction, then the function returns 'None'
    If there is, returns which side the opponent is w.r.t. the player's heading: "right" or "left"
    '''
    # if not opponentInRunway(player, reactionDistance=5):
    #     return None

    opponent = nearestOpponent(player)
    diff_y = opponent.position.y - player.position.y
    diff_x = opponent.position.x - player.position.x
    angleToOpponent = math.atan2(diff_y, diff_x)

    # undo atan2 +/- pi operation : https://stackoverflow.com/questions/35749246/python-atan-or-atan2-what-should-i-use
    if diff_y >= 0 and diff_x < 0:
        angleToOpponent += -math.pi
    if diff_y < 0 and diff_x < 0:
        angleToOpponent += math.pi

    if angleToOpponent < 0:
        return 'right'

    return 'left'


behavior dribble_evasive_zigzag(destination_point):
    angleToOpponent = nearestOpponentRelativePositionAhead(self)
    #print("dribble_evasive_zigzag angleToOpponent: ", angleToOpponent)
    current_heading = self.heading
    # print("dribble_evasive_zigzag's angleToOpponent: ", angleToOpponent)

    if angleToOpponent == 'right': 
        # if opponent on the right side ahead, evade to left
        point_to_evadeTo = self offset along (45 deg relative to current_heading) by 0 @ Range(10,15)
    elif angleToOpponent == 'left': 
        # if opponent on the left side, evade to right
        point_to_evadeTo = self offset along (-45 deg relative to current_heading) by 0 @ Range(10,15)
    else:
        # if there is no opponent in front, move straight to the destination point
        point_to_evadeTo = destination_point

    #print("point_to_evadeTo: ", point_to_evadeTo)
    if point_to_evadeTo != destination_point:
        #print("Move to point_to_evadeTo")
        do MoveToPosition(point_to_evadeTo) # zig behavior
        take ReleaseDirection()
    #print("Move to destination_point")
    do MoveToPosition(destination_point, sprint =True) # zag behavior
    #print("release")
    take ReleaseSprint()
    take ReleaseDirection()

behavior AimGoalCornerAndShoot():
    ''' 
    Only takes a shot if there is available left/right goalside region to shoot,
    otherwise, just hold position with the ball and exit this behavior
    '''
    #print("AimGoalCornerAndShoot")
    take ReleaseSprint()
    take ReleaseDirection()
    aimPoint = aimPointToShoot(self)
    is_player_rightTeam = self.team == "right"
    #print("aimPoint: ", aimPoint)

    if is_player_rightTeam:
        goal_leftside_aimPoint = left_goal_left_corner
        goal_rightside_aimPoint = left_goal_right_corner
    else:
        goal_leftside_aimPoint = right_goal_left_corner
        goal_rightside_aimPoint = right_goal_right_corner

    if aimPoint is None:
        #print("aimPoint is None")
        # if there is no aimpoint to shoot, by default then shoot towards 
        # the goal corner further away from the player
        left_corner_distance = distance from self to goal_leftside_aimPoint
        right_corner_distance= distance from self to goal_rightside_aimPoint
        if left_corner_distance > right_corner_distance:
            aimPoint = goal_leftside_aimPoint
        else:
            aimPoint = goal_rightside_aimPoint

    #print("aimPoint: ", aimPoint)
    take MoveTowardsPoint(aimPoint, self.position, is_player_rightTeam)
    take Shoot()
    take ReleaseSprint()
    take ReleaseDirection()
    #print("exit AimGoalCornerAndShoot")


behavior FollowObject(object_to_follow, terminate_distance=1, sprint=False):
    '''
    Let a player follow the object (e.g. Ball)'s position
    this behavior exits once the player is within "terminate_distance" from the "object_to_follow"
    '''
    is_player_rightTeam = self.team == "right"
    while True:
        #ball = simulation().game_ds.ball
        x = object_to_follow.position.x
        y = object_to_follow.position.y
        #print(x,y)

        self_x = self.position.x
        self_y = self.position.y

        distance = math.sqrt(((x-self_x)*(x-self_x)) + (y-self_y)*(y-self_y))

        if is_player_rightTeam:
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

behavior dribbleToAndShoot(destination_point, sprint=False, reactionDistance=None):
    if reactionDistance == None:
        reactionDistance = Range(10,15) if not sprint else Range(15, 20)
    else:
        reactionDistance = reactionDistance
    try:
        do MoveToPosition(destination_point)
    interrupt when opponentInRunway(self, reactionDistance=reactionDistance):
        #print("opponentInRunway")
        do dribble_evasive_zigzag(destination_point)
    interrupt when left_penaltyBox.containsPoint(self.position):
        #print("in penalty box")
        do AimGoalCornerAndShoot()


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
        #print("Warning: Player don't have ball for passing!")
        pass

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