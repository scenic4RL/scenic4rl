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
    opponent_team = "left" if player.team == "right" else "right"
    ds = simulation().game_ds
    player_list = ds.right_players if opponent_team == "right" else ds.left_players

    closest_dist = math.inf
    nearestOpponent = None
    for p in player_list:
        distance = distance from player to p
        if distance != 0 and distance < closest_dist:
            nearestOpponent = p
            closest_dist = distance
    return nearestOpponent

def nearestTeammate(player):
    player_team = player.team
    ds = simulation().game_ds
    player_list = ds.right_players if player_team == "right" else ds.left_players

    closest_dist = math.inf
    nearestTeammate = None
    for p in player_list:
        distance = distance from player to p
        if distance != 0 and distance < closest_dist:
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
    opponent_team = "left" if player.team == "right" else "right"
    ds = simulation().game_ds
    player_list = ds.right_players if opponent_team == "right" else ds.left_players

    radius = reactionDistance
    runwayRegion = SectorRegion(center=player.position, radius=radius, heading=player.heading, angle=math.pi/2)

    for p in player_list:
        if runwayRegion.containsPoint(p.position):
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
    current_heading = self.heading

    if angleToOpponent == 'right': 
        # if opponent on the right side ahead, evade to left
        point_to_evadeTo = self offset along (45 deg relative to current_heading) by 0 @ Range(10,15)
    elif angleToOpponent == 'left': 
        # if opponent on the left side, evade to right
        point_to_evadeTo = self offset along (-45 deg relative to current_heading) by 0 @ Range(10,15)
    else:
        # if there is no opponent in front, move straight to the destination point
        point_to_evadeTo = destination_point

    if point_to_evadeTo != destination_point:
        do MoveToPosition(point_to_evadeTo) # zig behavior
        take ReleaseDirection()

    do MoveToPosition(destination_point, sprint =True) # zag behavior
    take ReleaseSprint()
    take ReleaseDirection()

behavior AimGoalCornerAndShoot():
    ''' 
    Only takes a shot if there is available left/right goalside region to shoot,
    otherwise, just hold position with the ball and exit this behavior
    '''
    take ReleaseSprint()
    take ReleaseDirection()
    aimPoint = aimPointToShoot(self)
    is_player_rightTeam = self.team == "right"

    if is_player_rightTeam:
        goal_leftside_aimPoint = left_goal_left_corner
        goal_rightside_aimPoint = left_goal_right_corner
    else:
        goal_leftside_aimPoint = right_goal_left_corner
        goal_rightside_aimPoint = right_goal_right_corner

    if aimPoint is None:
        # if there is no aimpoint to shoot, by default then shoot towards 
        # the goal corner further away from the player
        left_corner_distance = distance from self to goal_leftside_aimPoint
        right_corner_distance= distance from self to goal_rightside_aimPoint
        if left_corner_distance > right_corner_distance:
            aimPoint = goal_leftside_aimPoint
        else:
            aimPoint = goal_rightside_aimPoint

    take MoveTowardsPoint(aimPoint, self.position, is_player_rightTeam)
    take Shoot()
    take ReleaseSprint()
    take ReleaseDirection()


behavior FollowObject(object_to_follow, terminate_distance=1, sprint=False):
    '''
    Let a player follow the object (e.g. Ball)'s position
    this behavior exits once the player is within "terminate_distance" from the "object_to_follow"
    '''
    is_player_rightTeam = self.team == "right"
    while True:
        x = object_to_follow.position.x
        y = object_to_follow.position.y

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
        do dribble_evasive_zigzag(destination_point)
    interrupt when left_penaltyBox.containsPoint(self.position):
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

