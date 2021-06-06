from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.behaviors import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 5
param deterministic = True
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True


behavior print_me():

	print(self, self.is_controlled)
	while True:
		if self.is_controlled:

			take Shoot()

		else:
			take NoAction()


ego = Ball at 26 @ 11

LeftGK at -99 @ 0, with behavior print_me()
LeftLB at -67.2 @  19.576, with behavior print_me()
LeftCB at -75  @    6.356, with behavior print_me()
LeftCB at -75  @  -6.3559, with behavior print_me()
LeftRB at -67.2 @ -19.576, with behavior print_me()
LeftCM at -43.4 @  10.568, with behavior print_me()
LeftCM at -43.4 @ -10.568, with behavior print_me()
LeftCM at  50 @ 31.61, with behavior print_me()
LeftLM at  25 @ 10, with behavior print_me()
LeftRM at  25 @ -10, with behavior print_me()
LeftCF at  35 @ -31.6102, with behavior print_me()


RightGK at 99 @ 0, with behavior print_me()
RightLB at -12 @ -21, with behavior print_me()
RightCB at -40 @ -6.356, with behavior print_me()
RightCB at  40 @ 6.3559, with behavior print_me()
RightRB at -13 @ -20, with behavior print_me()
RightCM at -36.5 @ -10.568, with behavior print_me()
RightCM at -28.2 @ 0, with behavior print_me()
RightCM at -36.5 @ 10.568, with behavior print_me()
RightLM at -54 @ -31.61, with behavior print_me()
RightRM at -51 @ 0.0, with behavior print_me()
RightCF at -54 @ 31.6102, with behavior print_me()
