from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator
from math import degrees
param game_duration = 400
param deterministic = True


ego = MyPlayer at (100-pbox_width) @ (pbox_height/2),
            with role "GK"
ball = Ball at ((100-pbox_width) @ (-1*pbox_height/2))


OpPlayer at 0@0, with role "GK"

print(right_pbox.position, right_pbox.corners, right_pbox.length, right_pbox.width)
print(ego.position, ball.position)
#Expected: MyGK at bottom left corner of penalty box
#MyGK at (around) top left corner of penalty box
