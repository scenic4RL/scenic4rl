from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator


param game_duration = 600
param deterministic = False


ego = MyPlayer at 0 @ 0,
            facing 270 deg,
            with role "CF"


