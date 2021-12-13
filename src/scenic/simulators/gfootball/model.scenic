"""Scenic World Model for GFootball Scenarios."""
import math

from scenic.simulators.gfootball.simulator import GFootBallSimulator
simulator GFootBallSimulator(timestep=0.1) #1 step is 100ms

#Constants
pos_inf = 500
eps = 0.001

"""Default Parameters"""

"""
default_scene_params = {
    'game_duration': 400,
    'deterministic': False,
    'offsides': False,
    'end_episode_on_score': True,
    'end_episode_on_out_of_play': False,
    'end_episode_on_possession_change': False,
    'right_team_difficulty': 0.0,
    'left_team_difficulty': 0.0
}
"""
#New Parameters
#param control_mode = "multi"
param manual_control = False

#CONFIG PARAMETERS
param action_set = 'v2'   # 'v2', 'default'
param custom_display_stats = None
param display_game_stats = True
param players =  ['agent:left_players=1', 'keyboard:right_players=1']
#param level =  '11_vs_11_stochastic'
param physics_steps_per_frame =  10
#param render = True
param render_resolution_x = 1280
param real_time =  True


#param level = "dynamic"
#GAME PARAMETERS #These parameters will only be written in the gfootball_scenari_file when explicitely specified in the scenic scenario
#param game_duration =  400
#param deterministic =  False
#param offsides =  False
#param end_episode_on_score =  False
#param end_episode_on_out_of_play =  False
#param end_episode_on_possession_change = False
#param right_team_difficulty  = 0.0
#param left_team_difficulty = 0.0

#Observation/RL Env Parameters
param stacked = False
param rewards = "scoring,checkpoints" # ['scoring', 'scoring,checkpoints']

#Logging parameters
param tracesdir = 'dumps'
param logdir = 'dumps'
param video_format =  'avi'
param video_quality_level= 0
param write_video = False
param write_goal_dumps = False #'If True, sampled traces after scoring are dumped.'
param write_full_episode_dumps = False #'If True, trace is dumped after every episode.'
param dump_full_episodes = False
param dump_scores = False
param dump_frequency = 0 # In runPPO2 dump_frequency = 50 was used


# Set up geometric attributes
field_width  = 200
field_height =  84
field_width_su = 2           #fieldWidth in terms of Simulator unit
field_height_su = 0.42*2

pbox_height = 48
pbox_width  = 29 # was set based on eyeballing by setting balls' location.. The simulator places a ball/a player in slightly different positions for some reason

#derived attributes
field_hw = field_width/2
field_hh = field_height/2

left_penaltyBox_center = -1 * (field_width / 2 - pbox_width / 2)
right_penaltyBox_center = -1 * left_penaltyBox_center

left_goal_midpoint = -(field_width/2) @ 0
right_goal_midpoint = (field_width/2) @ 0

left_goal_left_corner = -100 @ -2.76
left_goal_right_corner = -100 @ 2.76

right_goal_left_corner = 100 @ 3
right_goal_right_corner = 100 @ -3

goal_width = 0.1
#regions

workspace = Workspace(RectangularRegion(0 @ 0, 0, field_width, field_height))
right_goalRegion = RectangularRegion( (field_width-goal_width)/2 @ 0, 0, goal_width, 0.044*2*100)
my_goalRegion = RectangularRegion( -1*(field_width-goal_width)/2 @ 0, 0, goal_width, 0.044*2*100)

left_penaltyBox =  RectangularRegion(left_penaltyBox_center @ 0, 0, pbox_width, pbox_height)
right_penaltyBox = RectangularRegion(-1 * left_penaltyBox_center @ 0, 0 deg, pbox_width, pbox_height)

center = 0 @ 0
corner_tr = (field_hw@field_hh)
corner_bl = ((-1*field_hw)@(-1*field_hh))
corner_br = (field_hw@(-1*field_hh))
corner_tl = ((-1*field_hw)@field_hh)

def grid(r,c,grid_len=5):
    #assert r<slots/2,
    dx = field_width/grid_len
    dy = field_height/grid_len
    return RectangularRegion( ((r*dx)@(c*dy)), 0, dx, dy)

"""
goal - Left/right goal is located
    at -1 and 1 X coordinate,
    ranging -0.044 and 0.044  in y-Axis
"""


"""
class LeftGoalMidPoint:
class RightGoalMidPoint:
class Center:
"""
# types of objects

class Ball:
    #Ball State: https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
    #5 properties in GFootball: position, direction, rotation, owned_team, owned_player
    position[dynamic]: Point on workspace
    direction[dynamic]: 0 deg
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
    allowCollisions: False
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


class Player:
    #gfootball properties
    position[dynamic]: Point on workspace
    team: str
    #position_sim[dynamic]: Vector

    direction[dynamic]: 0 deg
    #direction_vec[dynamic]: Vector

    tired_factor[dynamic]: (0,1)#float
    yellow_cards[dynamic]: int
    red_card[dynamic]: False
    role[dynamic]: Uniform("GK", "CB", "LB", "RB", "DM", "CM", "LM", "RM", "AM", "CF")
    is_controlled[dynamic]: False

    #controlled[dynamic]: False #IS this the player controlled by RL/ User Logic
    #designated: False #dont need for single-agent, hence

    #in this link, it says action is a 10 element array, but actually it returns a 13 element array
    #https://github.com/google-research/football/blob/master/gfootball/doc/observation.md
    sticky_actions[dynamic]: list

    #G footbal derived
    owns_ball[dynamic]: False #whether he (as a result also his team) posses the ball or not

    #for interfacing
    #obs_index[dynami]

    #scenic properties
    heading: 0 deg
    width: 1.0
    length: 1.0
    allowCollisions: False
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

    """
    def __init__(self):
        if self.role is "CF":
            position[dynamic]: Point on StrikerZone
            # require position in StrikerZone
    """


class LeftPlayer(Player):
    pass

class RightPlayer(Player):
    pass


#source: https://github.com/google-research/football/blob/master/gfootball/scenarios/11_vs_11_competition.py
#("GK", "CB", "LB", "RB", "DM", "CM", "LM", "RM", "AM", "CF")


#LEFT_REGIONS

def get_reg_from_edges(left, right, top, bottom):
    cx = (left+right)/2
    cy = (top+bottom)/2
    h = math.fabs(top-bottom)
    w = math.fabs(right-left)

    return RectangularRegion(cx @ cy, 0, w, h)

field = workspace
right_half_field = get_reg_from_edges(0, 95, 38, -38)
right_bottom_half_field = get_reg_from_edges(0, 50, 38, -38)

left_half_field  = get_reg_from_edges(-95, 0, 38, -38)
left_bottom_half_field = get_reg_from_edges(-50, 0, 38, -38)

LeftReg_GK = get_reg_from_edges(-100, -98, 2, -2)

LeftReg_CB = get_reg_from_edges(-52, -48, 10, -10)
LeftReg_LB = get_reg_from_edges(-44, -42,  22,  18)
LeftReg_RB = get_reg_from_edges(-44, -42, -22, -18)

LeftReg_LM = get_reg_from_edges(-20, -16, 22, 18) #[(-0.01, -0.2161)],
LeftReg_CM = get_reg_from_edges(-26, -22, 5, -5)
LeftReg_RM = get_reg_from_edges(-20, -16, -22, -18) # [(0.00,  0.02)],

LeftReg_DM = get_reg_from_edges(-38, -32, 5, -5)

LeftReg_CML = get_reg_from_edges(-16, -20, 12, 8)
LeftReg_CMR = get_reg_from_edges(-16, -20, -12, -8)
LeftReg_CMM = get_reg_from_edges(-30, -24, 2, -2)

LeftReg_AM = get_reg_from_edges(-10, -15, 2, -2)
LeftReg_CF = get_reg_from_edges(-5, -1, 2, -2)


class LeftGK(LeftPlayer):
    position[dynamic]: Point on LeftReg_GK
    role[dynamic]: "GK"
    team: 'left'

class LeftLB(LeftPlayer):
    position[dynamic]: Point on LeftReg_LB
    role[dynamic]: "LB"
    team: 'left'

class LeftRB(LeftPlayer):
    position[dynamic]: Point on LeftReg_RB
    role[dynamic]: "RB"
    team: 'left'

class LeftCB(LeftPlayer):
    position[dynamic]: Point on LeftReg_CB
    role[dynamic]: "CB"
    team: 'left'

class LeftLM(LeftPlayer):
    position[dynamic]: Point on LeftReg_LM
    role[dynamic]: "LM"
    team: 'left'

class LeftDM(LeftPlayer):
    position[dynamic]: Point on LeftReg_DM
    role[dynamic]: "DM"
    team: 'left'

class LeftRM(LeftPlayer):
    position[dynamic]: Point on LeftReg_RM
    role[dynamic]: "RM"
    team: 'left'

class LeftCM(LeftPlayer):
    position[dynamic]: Point on LeftReg_CM
    role[dynamic]: "CM"
    team: 'left'

class LeftCMM(LeftPlayer):
    position[dynamic]: Point on LeftReg_CMM
    role[dynamic]: "CM"
    team: 'left'

class LeftCML(LeftPlayer):
    position[dynamic]: Point on LeftReg_CML
    role[dynamic]: "CM"
    team: 'left'

class LeftCMR(LeftPlayer):
    position[dynamic]: Point on LeftReg_CMR
    role[dynamic]: "CM"
    team: 'left'

class LeftCF(LeftPlayer):
    position[dynamic]: Point on LeftReg_CF
    role[dynamic]: "CF"
    team: 'left'

class LeftAM(LeftPlayer):
    position[dynamic]: Point on LeftReg_AM
    role[dynamic]: "AM"
    team: 'left'


RightReg_GK = get_reg_from_edges(100, 98, 2, -2)

RightReg_CB = get_reg_from_edges(52, 48, 10, -10)
RightReg_LB = get_reg_from_edges(44, 42,  -22,  -18)
RightReg_RB = get_reg_from_edges(44, 42, 22, 18)

RightReg_LM = get_reg_from_edges(20, 16, -22, -18) #[(-0.01, -0.2161)],
RightReg_CM = get_reg_from_edges(26, 22, 5, -5)
RightReg_RM = get_reg_from_edges(20, 16, 22, 18) # [(0.00,  0.02)],
RightReg_DM = get_reg_from_edges(38, 32, 5, -5)

RightReg_CML = get_reg_from_edges(16, 20, -12, -8)
RightReg_CMR = get_reg_from_edges(16, 20, 12, 8)
RightReg_CMM = get_reg_from_edges(30, 24, 2, -2)

RightReg_AM = get_reg_from_edges(10, 15, 2, -2)
RightReg_CF = get_reg_from_edges(5, 1, 2, -2)

class RightGK(RightPlayer):
    position[dynamic]: Point on RightReg_GK
    role[dynamic]: "GK"
    team: 'right'

class RightLB(RightPlayer):
    position[dynamic]: Point on RightReg_LB
    role[dynamic]: "LB"
    team: 'right'

class RightRB(RightPlayer):
    position[dynamic]: Point on RightReg_RB
    role[dynamic]: "RB"
    team: 'right'

class RightCB(RightPlayer):
    position[dynamic]: Point on RightReg_CB
    role[dynamic]: "CB"
    team: 'right'

class RightLM(RightPlayer):
    position[dynamic]: Point on RightReg_LM
    role[dynamic]: "LM"
    team: 'right'

class RightDM(RightPlayer):
    position[dynamic]: Point on RightReg_DM
    role[dynamic]: "DM"
    team: 'right'

class RightRM(RightPlayer):
    position[dynamic]: Point on RightReg_RM
    role[dynamic]: "RM"
    team: 'right'

class RightCM(RightPlayer):
    position[dynamic]: Point on RightReg_CM
    role[dynamic]: "CM"
    team: 'right'

class RightCMM(RightPlayer):
    position[dynamic]: Point on RightReg_CMM
    role[dynamic]: "CM"
    team: 'right'

class RightCML(RightPlayer):
    position[dynamic]: Point on RightReg_CML
    role[dynamic]: "CM"
    team: 'right'

class RightCMR(RightPlayer):
    position[dynamic]: Point on RightReg_CMR
    role[dynamic]: "CM"
    team: 'right'

class RightCF(RightPlayer):
    position[dynamic]: Point on RightReg_CF
    role[dynamic]: "CF"
    team: 'right'

class RightAM(RightPlayer):
    position[dynamic]: Point on RightReg_AM
    role[dynamic]: "AM"
    team: 'right'

MY_PLAYER_DEFAULT_POSITIONS = {
    "GK": [(-1.00, 0.00)],
    "CB": [(-0.50, -0.06356),(-0.500000, 0.06356)],
    "LB": [(-0.422, -0.19576)],
    "RB": [(-0.422,  0.19576)],
    "DM": [],
    "CM": [(-0.18421, -0.10568), (-0.26757, 0.00), (-0.18421, 0.10568)],
    "LM": [(-0.01, -0.2161)],
    "RM": [(0.00,  0.02)],
    "AM": [],
    "CF": [(0.00, -0.02)]
}

"""
builder.AddPlayer(-1.000000, 0.000000, e_PlayerRole_GK)
builder.AddPlayer(0.000000,  0.020000, e_PlayerRole_RM)
builder.AddPlayer(0.000000, -0.020000, e_PlayerRole_CF)
builder.AddPlayer(-0.422000, -0.19576, e_PlayerRole_LB)
builder.AddPlayer(-0.500000, -0.06356, e_PlayerRole_CB)
builder.AddPlayer(-0.500000, 0.063559, e_PlayerRole_CB)
builder.AddPlayer(-0.422000, 0.195760, e_PlayerRole_RB)
builder.AddPlayer(-0.184212, -0.10568, e_PlayerRole_CM)
builder.AddPlayer(-0.267574, 0.000000, e_PlayerRole_CM)
builder.AddPlayer(-0.184212, 0.105680, e_PlayerRole_CM)
builder.AddPlayer(-0.010000, -0.21610, e_PlayerRole_LM)
"""