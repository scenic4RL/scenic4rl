from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball import model
from scenic.core.vectors import Vector
import math

def pos_sim_to_scenic(pos):
    x = sim_to_scenic_x(pos[0])
    y = sim_to_scenic_y(pos[1])
    return Vector(x, y)


def scenic_to_sim_x(x):
    return model.field_width_su*x/model.field_width

def scenic_to_sim_y(y):
    return -1 * model.field_height_su*y/model.field_height

def sim_to_scenic_x(x):
    return model.field_width * x / model.field_width_su

def sim_to_scenic_y(y):
    return -1 * model.field_height * y / model.field_height_su


def pos_scenic_to_sim(pos):
    x = scenic_to_sim_x(pos.x)
    y = scenic_to_sim_y(pos.y)
    return Vector(x,y)


def get_angle_from_direction(direction):
    import math
    eps = 1e-5

    delx = direction[0]
    dely = direction[1]

    delx = sim_to_scenic_x(delx)
    dely = sim_to_scenic_y(dely)

    #delx = 3
    #dely = -1

    if -eps < delx < eps:
        angle = 90
    elif -eps < dely < eps:
        angle = 0
    else:
        angle = math.atan(dely / delx) * 180 / math.pi

    #print(angle)
    if delx < 0 and dely < 0:
        angle += 180
    elif angle < 0 and delx < 0:
        angle += 180
    elif angle < 0 and dely < 0:
        angle += 360

    #print(angle)

    #convert angle from +x axis to  + y axis
    angle = (angle - 90 + 360)%360
    #print(angle)
    return angle