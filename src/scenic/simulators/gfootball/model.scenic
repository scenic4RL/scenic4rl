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

#dbox = RectangularRegion(0.8 @ 0, 0, 0.4, 0.4)
penbox_width = 24
#penalty_right = RectangularRegion( ((field_width-penbox_width)/2) @ 0, 0, penbox_width, 40.32) #stanard dimensions used, need to check what gfootball uses
#penalty_left = RectangularRegion( ((-1*field_width+penbox_width)/2) @ 0, 0, penbox_width, 40.32)
penalty_left =  RectangularRegion( -88 @ 0, 0, penbox_width, 40.32) # -166/2+24/2 == -71
penalty_right = RectangularRegion( 88 @ 0, 0, penbox_width, 40.32)

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

class LeftGoalMidPoint:
    position: -(field_width/2) @ 0
    width: 0
    height: 0


class Center:
    position: 0@0
    #viewAngle: 360 deg
    #viewDistance: pos_inf

# types of objects

class Ball:
    position: Point on workspace
    direction: Range(0, 360) deg
    rotationX: Range(0, 360) deg
    rotationY: Range(0, 360) deg
    rotationZ: Range(0, 360) deg
    ball_owned_team: int
    ball_owned_player: int
    width: 0.2
    length: 0.2
    #askEddie: allowCollisions: True (???)
    allowCollisions: True
    requireVisible: False
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
    position: Point on workspace
    position_sim: Vector
    direction: Range(0, 360) deg
    direction_vec: Vector
    heading: Range(0, 360) deg
    allowCollisions: True
    #name: "player"


    tired_factor: float
    width: 0.5
    length: 0.5
    role: "CM"

    #active[dynamic] : False
    active: False
    designated: False
    ball_owned: False

    yellow_card: False
    red_card: False

    #askEddie: should be of action data type
    current_action: int
    requireVisible: False
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
