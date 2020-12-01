"""Scenic World Model for GFootball Scenarios."""

from scenic.simulators.gfootball.simulator import GFootBallSimulator

simulator GFootBallSimulator()

#Constants
pos_inf = 500
eps = 0.001

# Set up workspace
field_width  = 200           # Exact: 2 * 7.32/0.088  == 166.37 meter
field_height =  84           # Exact: 0.42 * 2 * 7.32 / 0.088 == 69.8727 Meter

field_width_su = 2           #fieldWidth in terms of Simulator unit
field_height_su = 0.42*2

workspace = Workspace(RectangularRegion(0 @ 0, 0, field_width, field_height))

penbox_height = 48
penbox_width  = 30

penalty_left_center = -1*(field_width/2 - penbox_width/2)
pbox_left =  RectangularRegion( penalty_left_center @ 0, 0, penbox_width, penbox_height)
pbox_right = RectangularRegion( -1*penalty_left_center @ 0, 180 deg, penbox_width, penbox_height)

left_goal_midpoint = -(field_width/2) @ 0
right_goal_midpoint = (field_width/2) @ 0
# top - left [-1, -0.42]
# bottom - right [1, 0.42]

"""
goal - Left/right goal is located
    at -1 and 1 X coordinate,
    ranging -0.044 and 0.044  in y-Axis

    y-axis height = 0.044*2 = 0.088

    #https://www.itsagoal.net/fifa-laws-of-the-game/
    #https://www.wikiwand.com/en/Football_pitch#:~:text=Goals%20are%20placed%20at%20the,8%20ft)%20above%20the%20ground.
    #https://www.quora.com/What-are-the-official-dimensions-of-a-soccer-field-in-the-FIFA-World-Cup
    #https://www.footballhistory.org/field.html 

    The inner edges of the posts must be 7.32 metres (8 yd) apart
    Standard field: 105 x 68
    hence,

    1 Y simulator unit = 7.32/0.088 meter
    1 meter  = 0.088/7.32  Y simulator unit
    height = 0.42*2 sm unit = 0.42 * 2 * 7.32 / 0.088 = 69.87272727272727 meter
    width = 2 * 7.32/0.088 = 166.36363636363637 meter
"""


#askEddie: How to define regions within workspace: Dbox, left half, right half, etc

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
