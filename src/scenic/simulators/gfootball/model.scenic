"""Scenic World Model for GFootball Scenarios."""
from scenic.simulators.gfootball.simulator import GFootBallSimulator
simulator GFootBallSimulator()

#Constants
pos_inf = 500
eps = 0.001

# Set up geometric attributes
field_width  = 200
field_height =  84
field_width_su = 2           #fieldWidth in terms of Simulator unit
field_height_su = 0.42*2


pbox_height = 48
pbox_width  = 29 # was set based on eyeballing by setting balls' location.. The simulator places a ball/a player in slightly different positions for some reason

#derived attributes
pbox_left_center = -1 * (field_width / 2 - pbox_width / 2)
pbox_right_center = -1 * pbox_left_center

left_goal_midpoint = -(field_width/2) @ 0
right_goal_midpoint = (field_width/2) @ 0

goal_width = 0.1
#regions

workspace = Workspace(RectangularRegion(0 @ 0, 0, field_width, field_height))

right_goal = RectangularRegion( (field_width-goal_width)/2 @ 0, 0, goal_width, 0.044*2*100)
left_goal = RectangularRegion( -1*(field_width-goal_width)/2 @ 0, 0, 0.1, 0.044*2*100)

left_pbox =  RectangularRegion(pbox_left_center @ 0, 0, pbox_width, pbox_height)
right_pbox = RectangularRegion(-1 * pbox_left_center @ 0, 0 deg, pbox_width, pbox_height)


"""
goal - Left/right goal is located
    at -1 and 1 X coordinate,
    ranging -0.044 and 0.044  in y-Axis
"""


"""
class LeftGoalMidPoint:
    position: -(field_width/2) @ 0
    width: 0
    height: 0
    heading: 0 deg

class RightGoalMidPoint:
    position: (field_width / 2) @ 0
    width: 0
    height: 0
    heading: 270 deg
    #heading: 270 deg



class Center:
    position: 0@0
    heading: 0 deg
    width: 0
    height: 0
    #viewAngle: 360 deg
    #viewDistance: pos_inf
    allowCollisions: True
    requireVisible: False
"""
# types of objects

class Ball:
    #Ball State: https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
    #5 properties in GFootball: position, direction, rotation, owned_team, owned_player
    position[dynamic]: Point on workspace
    direction[dynamic]: Range(0, 360) deg
    rotation[dynamic]: tuple
    owned_team[dynamic]: int
    owned_player_idx[dynamic]: int
    heading: 0 deg

    #rotationX: Range(0, 360) deg
    #rotationY: Range(0, 360) deg
    #rotationZ: Range(0, 360) deg

    #constant scenic properties
    width: 0.2
    length: 0.2
    allowCollisions: True
    requireVisible: False

    """
    viewAngle: 360 deg
    visibleDistance: pos_inf
    """

    """
    ball - [x, y, z] position of the ball.
    ball_direction - [x, y, z] ball movement vector.
    ball_rotation - [x, y, z] rotation angles in radians.
    ball_owned_team - {-1, 0, 1}, -1 = ball not owned, 0 = left team, 1 = right team.
    ball_owned_player - {0..N-1} integer denoting index of the player owning the ball.
    """

"""
Speed vectors represent a change in the position of the object within a single step.
"""

#AskEddie: How to modify distribution of position based on role?
class Player:
    #gfootball properties
    position[dynamic]: Point on workspace
    #position_sim[dynamic]: Vector

    direction[dynamic]: Range(0, 360) deg
    #direction_vec[dynamic]: Vector

    tired_factor[dynamic]: (0,1)#float
    yellow_cards[dynamic]: float
    red_card[dynamic]: False
    role[dynamic]: Uniform("GK", "CB", "LB", "RB", "DM", "CM", "LM", "RM", "AM", "CF")

    controlled[dynamic]: False #IS this the player controlled by RL/ User Logic
    #designated: False #dont need for single-agent, hence

    #in this link, it says action is a 10 element array, but actually it returns a 13 element array
    #https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
    sticky_actions[dynamic]: list

    #G footbal derived
    owns_ball[dynamic]: False #whether he (as a result also his team) posses the ball or not

    #scenic properties
    heading: 0 deg
    width: 0.5
    length: 0.5
    allowCollisions: True
    requireVisible: False

    viewAngle: 360 deg
    visibleDistance: pos_inf
    """
    left_team - N-elements vector with [x, y] positions of players.
    left_team_direction - N-elements vector with [x, y] movement vectors of players.
    left_team_tired_factor - N-elements vector of floats in the range {0..1}. 0 means player is not tired at all.
    left_team_yellow_card - N-elements vector of integers denoting number of yellow cards a given player has (0 or 1).
    left_team_active - N-elements vector of Bools denoting whether a given player is playing the game (False means player got a red card).
    left_team_roles - N-elements vector denoting roles of players. The meaning is:
    """


#AskEddie: should we specify a boolean field in player? instead of My/Op Player

class MyPlayer(Player):
    pass

class OpPlayer(Player):
    pass
