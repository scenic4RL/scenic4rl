from scenic.simulators.carla.map import setMapPath
setMapPath(__file__, 'OpenDrive/Town03.xodr')
from scenic.simulators.carla.road_model import *

ego = Car
Pedestrian on visible sidewalk