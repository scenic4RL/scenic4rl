from scenic.simulators.gfootball.model import *
from scenic.simulators.gfootball.simulator import GFootBallSimulator

param game_duration = 400
param deterministic = False
param offsides = False
param end_episode_on_score = True
param end_episode_on_out_of_play = True
param end_episode_on_possession_change = True

rightTeamInitialRegion = get_reg_from_edges(-15, -10, 40, -40)
leftCBInitialRegion = get_reg_from_edges(0, 5, 40, -40)

# Goalkeeper needs to be instantiated to avoid an error but we place them at a corner and stay there
RightGK at -90 @ 30, with behavior HoldPosition()
LeftGK at -90 @ 35, with behavior HoldPosition()

ego = LeftCB on leftCBInitialRegion
Ball ahead of ego by 2

RightLB on rightTeamInitialRegion
RightCB on rightTeamInitialRegion
RightCM on rightTeamInitialRegion
RightCB on rightTeamInitialRegion
RightRB on rightTeamInitialRegion