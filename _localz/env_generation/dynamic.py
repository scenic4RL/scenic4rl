from . import *


data_path = "/Users/azadsalam/codebase/scenic/_localz/env_generation/data"





def build_scenario(builder):
  with open(data_path, "r+") as f:
    x = float(f.readline())
    y = float(f.readline())
    print(x, y)


  builder.config().game_duration = 400
  builder.config().deterministic = False
  builder.config().offsides = False
  builder.config().end_episode_on_score = True
  builder.config().end_episode_on_out_of_play = True
  builder.config().end_episode_on_possession_change = True
  builder.SetBallPosition(x, y)

  builder.SetTeam(Team.e_Left)
  builder.AddPlayer(-1.0, 0.0, e_PlayerRole_GK)
  builder.AddPlayer(0.0, 0.0, e_PlayerRole_CB)

  builder.SetTeam(Team.e_Right)
  builder.AddPlayer(1.0, 0.0, e_PlayerRole_GK)
  builder.AddPlayer(0.12, 0.2, e_PlayerRole_LB)
  builder.AddPlayer(0.12, 0.1, e_PlayerRole_CB)
  builder.AddPlayer(0.12, 0.0, e_PlayerRole_CM)
  builder.AddPlayer(0.12, -0.1, e_PlayerRole_CB)
  builder.AddPlayer(0.12, -0.2, e_PlayerRole_RB)