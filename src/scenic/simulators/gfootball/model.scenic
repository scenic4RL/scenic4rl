"""Scenic World Model for GFootball Scenarios."""

from scenic.simulators.gfootball.simulator import GFootBallSimulator

simulator GFootBallSimulator()

# Set up workspace
width  = 2 * 7.32/0.088           # 166.37 meter
height = 0.42 * 2 * 7.32 / 0.088  # 69.8727 Meter
workspace = Workspace(RectangularRegion(0 @ 0, 0, width, height)) #ask eddie about first two parameters

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

    The inner edges of the posts must be 7.32 metres (8 yd) apart
    Standard: 110 x 68
    hence,

    1 Y simulator unit = 7.32/0.088 meter
    1 meter  = 0.088/7.32  Y simulator unit
    height = 0.42*2 sm unit = 0.42 * 2 * 7.32 / 0.088 = 69.87272727272727 meter
    width = 2 * 7.32/0.088 = 166.36363636363637 meter




"""


dbox = RectangularRegion(0.8 @ 0, 0, 0.4, 0.4)

#askEddie: How to define regions within workspace: Dbox, left half, right half, etc


# types of objects

class Ball:
    position: Point on workspace
    direction: Range(0, 360) deg
    rotationX: Range(0, 360) deg
    rotationY: Range(0, 360) deg
    rotationZ: Range(0, 360) deg
    ball_owned_team: int
    ball_owned_player: int
    width: 0.005
    length: 0.005


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
    direction: Range(0, 360) deg
    tired_factor: float
    width: 0.01
    length: 0.01
    role: "CM"

    active: False
    designated: False
    ball_owned: False

    yellow_card: False
    red_card: False

    #askEddie: should be of action data type
    current_action: int

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
