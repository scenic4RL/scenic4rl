from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball import model
from scenic.core.vectors import Vector

def pos_sim_to_scenic(pos):
    x = sim_to_scenic_x(pos[0])
    y = -1*sim_to_scenic_y(pos[1])
    return Vector(x, y)


def scenic_to_sim_x(x):
    return model.field_width_su*x/model.field_width

def scenic_to_sim_y(y):
    return model.field_height_su*y/model.field_height

def sim_to_scenic_x(x):
    return model.field_width * x / model.field_width_su

def sim_to_scenic_y(y):
    return model.field_height * y / model.field_height_su


def pos_scenic_to_sim(pos):
    x = scenic_to_sim_x(pos.x)
    y = -1*scenic_to_sim_y(pos.y)
    return Vector(x,y)

